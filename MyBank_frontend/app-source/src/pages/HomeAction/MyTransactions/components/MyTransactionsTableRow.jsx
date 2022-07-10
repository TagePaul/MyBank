import React from "react"

const MyTransactionsTableRow = (props) => {
    return (
        <tr>
            <td>{props.id}</td>
            <td>{props.status}</td>
            <td>{props.transfer_from_bank_account}</td>
            <td>{props.transfer_to_bank_account}</td>
            <td>{props.transfer_amount}</td>
        </tr>
    )

}

export default MyTransactionsTableRow;