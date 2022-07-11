const mode = 'Docker.prod' // 'Docker.dev' 'Docker.prod'/ 'Local'

let HOST = null

if (mode == 'Docker.dev') {
    HOST = 'http://localhost'
} else if (mode == 'Local') {
    HOST = 'http://localhost:8000'
} else if (mode == 'Docker.prod') {
    HOST = 'http://194.87.248.96'
}

export const APIRegister = `${HOST}/api/users/register/`
export const APILogin = `${HOST}/api/jwt/create/`
export const APIIsAuth = `${HOST}/api/jwt/verify/`
export const APIRefresh = `${HOST}/api/jwt/refresh/`

export const APIGetBalance = `${HOST}/api/bl/my_balance/`

export const APITransact = `${HOST}/api/ts/transact/`
export const APIConfirmTransact = `${HOST}/api/ts/confirm_transact/?confirm_token=`
export const APIMyTransactions = `${HOST}/api/ts/my_transactions/`
export const APIAddMoney = `${HOST}/api/bl/adding_money/`
