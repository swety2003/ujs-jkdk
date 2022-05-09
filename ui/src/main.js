import Vue from 'vue'
import App from './App.vue'
import './plugins/element.js'
import axios from 'axios';
import Router from 'vue-router' // 引入vue-router
import router from './router'
Vue.config.productionTip = false
Vue.prototype.$login=true;
Vue.use(Router)



Vue.prototype.$axios = axios;

//异步请求前在header里加入token
axios.interceptors.request.use(
  config => {
      if (localStorage.getItem('token')) {
        config.headers.authorization ="Bearer "+ localStorage.getItem('token');
      }
    
    return config;
  },
  error => {
    return Promise.reject(error);
  });
// 异步请求后，判断token是否过期
axios.interceptors.response.use(
  response =>{
    return response;
  },
  error => {
    if(error.response){
      switch (error.response.status) {
        case 401:
          localStorage.removeItem('token');
          
          router.push("/login")
      }
    }
  }
)



new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
