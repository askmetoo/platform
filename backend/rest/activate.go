package rest

import (
	"encoding/json"
	"github.com/syncloud/platform/activation"
	"github.com/syncloud/platform/rest/model"
	"net/http"
)

type ManagedActivation interface {
	Free(redirectEmail string, redirectPassword string, requestDomain string, deviceUsername string, devicePassword string) error
	Premium(redirectEmail string, redirectPassword string, requestDomain string, deviceUsername string, devicePassword string) error
}

type CustomActivation interface {
	Activate(requestDomain string, deviceUsername string, devicePassword string) error
}

type Activate struct {
	managed ManagedActivation
	custom  CustomActivation
}

func NewActivateBackend(free ManagedActivation, custom CustomActivation) *Activate {
	return &Activate{
		managed: free,
		custom:  custom,
	}
}

func (a *Activate) Custom(req *http.Request) (interface{}, error) {
	var request activation.CustomActivateRequest
	err := json.NewDecoder(req.Body).Decode(&request)
	if err != nil {
		return nil, err
	}
	err = validate(request.DeviceUsername, request.DevicePassword)
	if err != nil {
		return nil, err
	}
	return "ok", a.custom.Activate(request.Domain, request.DeviceUsername, request.DevicePassword)
}

func (a *Activate) Free(req *http.Request) (interface{}, error) {
	var request activation.ManagedActivateRequest
	err := json.NewDecoder(req.Body).Decode(&request)
	if err != nil {
		return nil, err
	}
	err = validate(request.DeviceUsername, request.DevicePassword)
	if err != nil {
		return nil, err
	}
	return "ok", a.managed.Free(request.RedirectEmail, request.RedirectPassword, request.Domain, request.DeviceUsername, request.DevicePassword)
}

func (a *Activate) Premium(req *http.Request) (interface{}, error) {
	var request activation.ManagedActivateRequest
	err := json.NewDecoder(req.Body).Decode(&request)
	if err != nil {
		return nil, err
	}
	err = validate(request.DeviceUsername, request.DevicePassword)
	if err != nil {
		return nil, err
	}
	return "ok", a.managed.Premium(request.RedirectEmail, request.RedirectPassword, request.Domain, request.DeviceUsername, request.DevicePassword)
}

func validate(username string, password string) error {
	if len(username) < 3 {
		return model.SingleParameterError("device_username", "less than 3 characters")
	}
	if len(password) < 7 {
		return model.SingleParameterError("device_password", "less than 7 characters")
	}
	return nil
}
