import { APIRegister } from '../API/API'

export async function registerDataIsValid(target) {
    try {
        let response = await fetch(APIRegister, {
            method: 'POST',
            body: new FormData(target),
        });
        if (response.status == 200) {
            let result = await response.json()
            let result_for_alert = {
                status: result.status,
                description: result.description
            }
            return result_for_alert
        } else {
            return {status: 'error',
                    description: 'Ошибка'}
        }
    } catch {
        return {status: 'error',
        description: 'Ошибка'}
    }

} 