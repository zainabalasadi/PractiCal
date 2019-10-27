import React from 'react';
import { HashRouter, Route, hashHistory } from 'react-router-dom';

import Calendar from './components/Calendar';





export default (
    <HashRouter history={hashHistory}>
        <div>
            <Calendar />
            
        </div>
    </HashRouter>
);
