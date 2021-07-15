package job

import (
	"fmt"
	"sync"
)

type Master struct {
	mutex  *sync.Mutex
	status JobStatus
	job    func()
}

func NewMaster() *Master {

	master := &Master{
		mutex:  &sync.Mutex{},
		status: JobStatusIdle,
	}
	return master
}

func (master *Master) Status() JobStatus {
	master.mutex.Lock()
	defer master.mutex.Unlock()
	return master.status
}

func (master *Master) Offer(job func()) error {
	master.mutex.Lock()
	defer master.mutex.Unlock()
	if master.status == JobStatusIdle {
		master.status = JobStatusWaiting
		master.job = job
		return nil
	} else {
		return fmt.Errorf("busy")
	}
}

func (master *Master) Take() (func(), error) {

	master.mutex.Lock()
	defer master.mutex.Unlock()
	if master.status == JobStatusWaiting {
		master.status = JobStatusBusy
		return master.job, nil
	} else {
		return nil, fmt.Errorf("no tasks")
	}
}

func (master *Master) Complete() error {
	master.mutex.Lock()
	defer master.mutex.Unlock()
	if master.status == JobStatusBusy {
		master.status = JobStatusIdle
		master.job = nil
		return nil
	} else {
		return fmt.Errorf("nothing to complete")
	}

}
