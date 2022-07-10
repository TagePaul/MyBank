import React , { useEffect , useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../../context";
import { getMyTransactions, myBalance } from "../../utils/HomeActionTool/HomeActionTool";
import MyTransactionsTableRow from "./MyTransactions/components/MyTransactionsTableRow";


const MyTransactions = () => {
    const redirect = useNavigate()
    const {isAuth, setIsAuth, proms} = useContext(AuthContext)
    const [myTransactions, setMyTransactions] = useState(null)

    useEffect(() => {
        if (isAuth == false) {
            redirect('/login')
        }
    })
    if (isAuth == true && myTransactions == null) {
        console.log(isAuth)
        console.log(myTransactions)
        getMyTransactions().then(result => {
            console.log(result)
            if (result) {
                setMyTransactions(result)
            } else {
                setMyTransactions(false)
            }
        })
    }

    let table = undefined
    if (isAuth == true && myTransactions) {
        if (myTransactions.length >= 1) {
            let table_context = myTransactions
            table = table_context.map((item, index) =>
                <MyTransactionsTableRow key={index} {...item} />)
        }
    }
    

    return (
        <div className="AllContentBox__ContentWorkArea ContentWorkArea">
            <div className="ContentWorkArea__MyTransactions MyTransactions">
                <div className="MyTransactions__title">
                    Мои транзакции
                </div>
                <table className="MyTransactions__table">
                    <th>id</th>
                    <th>Статус</th>
                    <th>Счет отправителя</th>
                    <th>Счет получателя</th>
                    <th>Сумма</th>
                    {table}
                </table>
            </div>
        </div>
    );
};

export default MyTransactions;