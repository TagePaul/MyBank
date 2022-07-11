import { APIGetBalance, 
         APITransact, 
         APIConfirmTransact,
         APIMyTransactions,
         APIAddMoney } from '../../API/API'

export async function myBalance(access_token) {
    try {
        let response = await fetch(APIGetBalance, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${access_token}` 
            }
        });
        if (response.status == 200) {
            let result = await response.json()
            return result.data.balance
        } else {
            return false
        }
    } catch {
        return false
    }
}

export async function transact(data) {
    try{
        let response = await fetch(APITransact, {
            method: 'POST',
            body: new FormData(data),
            headers: {
                Authorization: `Token ${localStorage.getItem('access')}`
            }
        });
        if (response.status == 200) {
            let result = await response.json()
            return result
        } else {
            return {'status': 'error', description: 'Ошибка'}
        }
    } catch(e) {
        return {'status': 'error', description: 'Ошибка'}
    }
}

export async function confirmTransact(data, token) {
    try{
        let response = await fetch(APIConfirmTransact + token, {
            method: 'POST',
            body: new FormData(data),
            headers: {
                Authorization: `Token ${localStorage.getItem('access')}`,
            }
        });
        if (response.status == 200) {
            let result = await response.json()
            return result
        } else {
            return {'status': 'error', description: 'Ошибка'}
        }
    }catch {
        return {'status': 'error', description: 'Ошибка'}
    }
}

export async function getMyTransactions() {
    try {
        let response = await fetch(APIMyTransactions, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Token ${localStorage.getItem('access')}`,
            }
        });
        if (response.status == 200) {
            let result = await response.json()
            return result
        } else {
            return false
        }
    } catch {
        return false
    }
}

export async function addMoney() {
    let response = await fetch(APIAddMoney, {
        method: 'GET',
        headers: {
            Authorization: `Token ${localStorage.getItem('access')}`,
        }
    })
}