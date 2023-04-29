import axios from 'axios'


export const AddJiratask = data => {
    return axios({ url: '/api/testrunner/jiraschedule/', method: 'POST', data: data })
};



export const UpdateJiratask = (url, data) => {
    return axios({ url: '/api/testrunner/jiraschedule/' + url + '/', method: 'PATCH', data: data })
};

export const GetJiratasklist = params => {
    return axios.get('/api/testrunner/jiraschedule/', params).then(res => res.data)
};
export const getJiraTaskPaginationBypage = params => {
    return axios.get('/api/testrunner/jiraschedule/', params).then(res => res.data)
};
export const DeleteJiratask = (url, params) => {
    return axios.delete('/api/testrunner/jiraschedule/' + url + '/', params)
};
export const DeleteAllJiraTask = data => {
    return axios.delete('/api/testrunner/jiraschedule/-1/', data)
};
export const runJIRAScheduleTest = params => {
    return axios.get('/api/testrunner/run_jiraschedule_test/', params).then(res => res.data)
};