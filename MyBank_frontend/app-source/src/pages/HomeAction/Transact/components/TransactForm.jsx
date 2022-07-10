import React from "react"

const TransactForm = (props) => {
    return (
        <div>
            <div className="ContentWorkArea__TransactBox TransactBox">
                 <div className="TransactBox__title">
                     Перевод по номеру телефона
                 </div>
                 <div className="TransactBox__Alert">
                    {props.resultSubmit !== null && props.resultSubmit.status == 'error'
                       ? <p>{props.resultSubmit.description}</p>
                       : null
                    }
                 </div>
                 <div className="TransactBox__form">
                     <form onSubmit={props.onSubmit}>
                        {props.field}
                     </form>
                 </div>
             </div>
        </div>
    )
}

export default TransactForm