import axios from 'axios'


export const addTask = (params, data) => {
    return axios({ url: '/api/testrunner/schedule/', method: 'POST', params: params, data: data })
};

export const copySchedule = (params, data) => {
    return axios({ url: '/api/testrunner/schedule/', method: 'POST', params: params, data: data })
};

export const updateTask = (url, params, data) => {
    return axios({ url: '/api/testrunner/schedule/' + url + '/', method: 'PATCH', params: params, data: data })
};

export const taskList = params => {
    return axios.get('/api/testrunner/schedule/', params).then(res => res.data)
};
export const getTaskPaginationBypage = params => {
    var url_str = '/api/testrunner/schedule/?page='+params.params.page+"&project="+params.params.project
    return axios.get(url_str).then(res => res.data)
};
export const deleteTasks = (url, params) => {
    return axios.delete('/api/testrunner/schedule/' + url + '/', params)
};
export const deleteSelectTasks = (params, data) => {
    return axios.delete('/api/testrunner/schedule/del/', { params: params, data: data })
};


export const runScheduleTest = (url,params) => {
    return axios.get('/api/testrunner/run_schedule_test/' + url + '/',params)
};
