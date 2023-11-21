import React from 'react';
import { AgGridReact } from 'ag-grid-react';
import useExpenses from '../hooks/useExpenses';

import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";

const ToDo = () =>{
    const {expenses, columnDefinitions} = useExpenses();
    return (
        <div className="ag-theme-alpine" style={{height: '50%', width: '100%'}}>
        <AgGridReact rowData={expenses} columnDefs={columnDefinitions}/>            
    </div>
    );
}
export default ToDo;