import { APIIsAuth, APIRefresh, APILogin } from '../API/API.js'

export async function checkAccessToken(access) {
    let access_token = {
      token: access
    }
    let response = await fetch(APIIsAuth, {
      method: 'POST',
      body: JSON.stringify(access_token),
      headers: {
        'Content-Type': 'application/json'
      }
    });
    if (response.status == 200) {
      return true
    } else {
        return false
    }
  }

export async function request_for_refresh_token (refresh) {
    let refresh_token = {
        refresh: refresh
    }
    let response = await fetch(APIRefresh, {
        method: 'POST',
        body: JSON.stringify(refresh_token),
        headers: {
        'Content-Type': 'application/json'
        }
    });
    if (response.status == 200) {
        let data = await response.json()
        localStorage.setItem('refresh', data.refresh)
        localStorage.setItem('access', data.access)
        return true
    } 
}

export async function login(target) {
  try {
    let response = await fetch(APILogin, {
      method: 'POST',
      body: new FormData(target)
    });
    if (response.status == 200 ) {
      let data = await response.json()
      localStorage.setItem('refresh', data.refresh)
      localStorage.setItem('access', data.access)
      return true
    } else {
      return false
    }
  } catch {
      return false
  }
}