import React from 'react';
import axios from 'axios';

<>
<script src="https://unpkg.com/react@17/umd/react.development.js" crossorigin></script>
<script src="https://unpkg.com/react-dom@17/umd/react-dom.development.js" crossorigin></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
</>


export default class SubLinks extends React.Component {
    render() {
        return (
            <h2>
                <ul id = "subLinkUl">
                    <li id = "subLinkLi"><a className="active" href="{{ url_for('home') }}">Home</a></li>
                    <li id = "subLinkLi"><a href="portfolio">Portfolio</a></li>
                    <li id = "subLinkLi"><a href="watchlist">Watchlist</a></li>
                    <li id = "subLinkLi" style={ {float:"right"}}>
                        <form action="/stockinfo" method="post">
                            <input type="text" name="ticker" placeholder="Enter ticker"/>
                            <input type="submit" value="Search"/>
                        </form>
                    </li>
                    if(session) {
                        <li id = "subLinkLi" style={ {float:"right"}}><a href="{{url_for('logout')}}">Logout</a></li>
                    } else {
                        <li id = "subLinkLi" style={ {float:"right"}}><a href="{{url_for('login')}}">Login</a></li>
                    }
                </ul>
            </h2>
        );
    }
}

/*
{% if session %}
<li style={ {float:"right"}}><a href="{{url_for('logout')}}">Logout</a></li>
{% else %}
<li style={ {float:"right"}}><a href="{{url_for('login')}}">Login</a></li>
{% endif %}
*/
 