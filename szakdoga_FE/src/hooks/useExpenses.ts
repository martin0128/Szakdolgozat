import { useEffect, useState } from 'react';
import axios from 'axios';
import { Expense } from '../model/expense';
import moment from 'moment';
import { ICellRendererParams } from 'ag-grid-community';

const useExpenses = () => {
    const [expenses, setExpenses] = useState<Expense[]>([]);
    const [columnDefinitions, setColumnDefinitions] = useState([
        {field: 'name'},
        {field: 'description'},
        {field: 'price'},
        {field: 'invoiceDate', cellRenderer: (data: ICellRendererParams) => {
            return moment(data.value).format('MM/DD/YYYY')
        }},
    ])

    useEffect(() => {
        axios.get<Expense[]>('/api/Expense/GetAll').then(res => setExpenses(res.data))
    },[])
    return {expenses, columnDefinitions, setColumnDefinitions};
}

export default useExpenses;