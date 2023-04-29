//资料库相关接口
import axios from 'axios'


export const uploadFile = params => {
    return config.baseurl + '/api/testrunner/file/'
};

export const downloadTestdata = params => {
    return axios.post('/api/testrunner/download/', params, { responseType: 'blob' })
};

export const testdataList = params => {
    return axios.get('/api/testrunner/file/', params).then(res => res.data)
};

export const getTestdataListPaginationBypage = params => {
    var url_str = '/api/testrunner/file/?page='+params.page+"&project="+params.project+"&search="+params.search
    return axios.get(url_str).then(res => res.data)
};

export const deleteTestdata = (url, params) => {
    return axios.delete('/api/testrunner/file/' + url + '/', params)
};

export const delAllTestdata = (params, data) => {
    return axios.delete('/api/testrunner/file/del/', { params, data })
};
export const lockFile = (params, data) => {
    return axios({ url: '/api/testrunner/lock_file/', method: 'POST', params: params, data: data })
};
export const exportvariable = params => {
    return axios.post('/api/testrunner/exportVariables/', params, { responseType: "blob" })
};
export const importvariable = params => {
    return config.baseurl + '/api/testrunner/importvariables/'
};

//文件数据核对相关接口
export const getDataContrastPaginationBypage = params => {
    return axios.get('/api/testrunner/datacontrast/', params).then(res => res.data)
};
export const addDataContrast = params => {
    return axios.post('/api/testrunner/datacontrast/', params).then(res => res.data)
};

export const updateDataContrast = (url, params) => {
    return axios.patch('/api/testrunner/datacontrast/' + url + '/', params).then(res => res.data)
};

export const DataContrastList = params => {
    return axios.get('/api/testrunner/datacontrast/', params).then(res => res.data)
};

export const delDataContrast = url => {
    return axios.delete('/api/testrunner/datacontrast/' + url + '/').then(res => res.data)
};

export const delAllDataContrast = params => {
    return axios.delete('/api/testrunner/datacontrast/', params).then(res => res.data)
};
export const RunDataContrastById = (url, params) => {
    return axios.get('/api/testrunner/run_datacontrast_pk/' + url + '/', params).then(res => res.data)
};