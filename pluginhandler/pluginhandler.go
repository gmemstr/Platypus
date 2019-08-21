package pluginhandler

import (
	"errors"
	"fmt"
	"github.com/containous/yaegi/interp"
	"github.com/go-yaml/yaml"
	"io/ioutil"
	"regexp"
	"strings"
)

var Plugins map[string] Plugin
// @TODO: This will cache for available hooks for a hook.
var PluginsForHooks map[string] HookFunc

type Plugin struct {
	Name string `yaml:"name"`
	Version string `yaml:"version"`
	Homepage string `yaml:"homepage"`
	ImplementsHooks []HookFunc
}

type HookFunc struct {
	Type string
	Name string
	Func string
}

// Searches through plugins directory and registers plugins with a valid
// plugin.yml file. Should only be run at startup.
// @TODO: Investigate reloading?
func RegisterPlugins() {
	Plugins = make(map[string]Plugin)

	plugins, err := ioutil.ReadDir("plugins")
	if err != nil {
		fmt.Println("Unable to read plugins directory")
		return
	}

	for _, plugin := range plugins {
		pluginName := plugin.Name()
		registeredPlugin, ok := Plugins[pluginName]
		// Already registered.
		if ok {
			continue
		}

		registeredPlugin = Plugin{}
		pluginInfo, err := ioutil.ReadFile("plugins/" + pluginName + "/plugin.yml")
		err = yaml.Unmarshal(pluginInfo, &registeredPlugin)
		// Malformed plugin.yml, @TODO log this somewhere for debugging
		if err != nil {
			continue
		}

		pluginContents, err := ioutil.ReadFile("plugins/" + pluginName + "/plugin.go")
		if err != nil {
			continue
		}
		pluginContent := string(pluginContents)

		hookRe := regexp.MustCompile(`((func)\s\w+\(.*\)(\s|.)*{(\s|.)*})`)
		funcs := hookRe.FindStringSubmatch(pluginContent)

		for _, funcContent := range funcs {
			re := regexp.MustCompile(`((func)\s\w+)`)
			foundFuncName := re.FindStringSubmatch(pluginContent)
			realFuncName := strings.TrimLeft(foundFuncName[1], "func ")

			hookFunc := HookFunc{
				Type: "something",
				Name: realFuncName,
				Func: funcContent,
			}

			registeredPlugin.ImplementsHooks = append(registeredPlugin.ImplementsHooks, hookFunc)
		}
		Plugins[pluginName] = registeredPlugin
	}

}

// Loop through registered plugins and execute any that match the hook.
func ExecuteHook(data string, hook string) string {
	for _, plugin := range Plugins {
		for _, hookImplementor := range plugin.ImplementsHooks {
			if hookImplementor.Type == hook {
				// @TODO: Handle errors :(
				data, _ = executePlugin(data, hookImplementor)
			}
		}
	}

	return data
}

// Execute a plugins hook function, and return the string result.
func executePlugin(data string, hook HookFunc) (string, error) {
	result := data
	interpreter := interp.New(interp.Options{})
	_, err := interpreter.Eval(hook.Func)
	if err != nil {
		return result, err
	}
	function, err := interpreter.Eval(hook.Name)
	if err != nil {
		return "", err
	}

	callable, ok := function.Interface().(func(string) string)
	if !ok {
		return "", errors.New("type does not match")
	}

	result = callable(data)

	return result, nil
}

