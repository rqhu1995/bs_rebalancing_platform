import HttpRequest from '@/libs/axios'
import config from '@/config'
const baseUrl = process.env.NODE_ENV === 'development' ? config.baseUrl.dev : config.baseUrl.pro

const axios = new HttpRequest(baseUrl)
export default axios

export const getTableData = () => {
  return axios.request({
    url: 'http://localhost:5000/station_info',
    method: 'get'
  })
}
