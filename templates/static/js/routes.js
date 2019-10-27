import React from 'react';
import { HashRouter, Route, hashHistory } from 'react-router-dom';

// Components
import Cal from './components/Calendar';


export default (
    <HashRouter>
        <div>
            <Route path="/" component={Cal}/>  
        </div>
    </HashRouter>
);
