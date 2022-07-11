import React, { useState, 
                useContext, 
                useEffect } from "react";
import { useNavigate } from "react-router-dom";

import { AuthContext } from "../../../context";
import Input_v1 from '../../../components/UI/Input/Input_v1'
import TransactForm from "./components/TransactForm";
import { transact, confirmTransact } from "../../../utils/HomeActionTool/HomeActionTool";

const Transact_v1 = () => {
    const redirect = useNavigate()
    let {isAuth, setIsAuth} = useContext(AuthContext)
    const [resultSubmitTransactFrom, 
           setResultSubmitTransactForm] = useState(null)
    const [resultSubmitTransactConfirmForm, 
           setResultTransactConfirmForm] = useState(null)
    useEffect(() => {
    if (isAuth == false) {
        redirect('/login')
        }
    })

    const transactFormContextForFields = [
        {
            'type': 'text', 'name': 'phone_number', 
            required: true, placeholder: 'Номер телефона', 
            pattern: "[0-9]{11}"
        },
        {
            'type': 'text', 'name': 'transfer_amount', 
            required: true, placeholder: 'Сумма перевода'
        },
        {
            'type': 'submit'
        }
    ]
    const transactFormFields = transactFormContextForFields.map(
            (item, index) =>
                <Input_v1 key={index} {...item} />)

    async function submitTransactFormEvent(event) {
        event.preventDefault()
        let target = event.target
        await transact(target).then((result) => {
            setResultSubmitTransactForm(result)
        })}


    const confirmTransactFormContextForFields = [
        {
            'type': 'text', 'name': 'secret_key', 
            required: true, placeholder: 'Код подтверждения'
        },
        {
            'type': 'submit'
        }
    ]
    const confirmTransactFormFields = confirmTransactFormContextForFields.map(
            (item, index) => 
                <Input_v1 key={index} {...item} />)

    async function submitConfirmTransactFormEvent(event) {
        event.preventDefault()
        let target = event.target
        let token = resultSubmitTransactFrom.data.query_params_confirm_token
        await confirmTransact(target, token).then((result) => {
            console.log(result)
            if (result.status == 'ok') {
                setResultSubmitTransactForm(null)
                setResultTransactConfirmForm(null)
            } else {
                setResultTransactConfirmForm(result)
            }
        })
    }

    let myForm = null
    if (resultSubmitTransactFrom == null || resultSubmitTransactFrom.status == 'error') {
        myForm = <TransactForm resultSubmit={resultSubmitTransactFrom} 
                      field={transactFormFields} 
                      onSubmit={submitTransactFormEvent}/>
    } else if (resultSubmitTransactFrom.status == 'ok') {
        myForm = <TransactForm resultSubmit={resultSubmitTransactConfirmForm}
                      field={confirmTransactFormFields}
                      onSubmit={submitConfirmTransactFormEvent}/>
    }
    return (
        <div className="AllContentBox__ContentWorkArea ContentWorkArea">
            {myForm}
        </div>
    )
}

export default Transact_v1
