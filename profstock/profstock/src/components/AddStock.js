import React from 'react';
import axios from 'axios';

<>
<script src="https://unpkg.com/react@17/umd/react.development.js" crossorigin></script>
<script src="https://unpkg.com/react-dom@17/umd/react-dom.development.js" crossorigin></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
</>

export default class AddStock extends React.Component {
    state = {
        ticker: ''
    }

    handleChange = event => {
        this.setState({ ticker: event.target.value });
    }

    handleSubmit = event => {
        event.preventDefault();

        const stock = {
            ticker: this.state.name
        };
        axios.post(`https://jsonplaceholder.typicode.com/users`, { stock })
      .then(res => {
        console.log(res);
        console.log(res.data);
      })
    }

    render() {
        return(
            <div>
                <form onSubmit={this.handleSubmit}>
                <input type="hidden" name="ticker"></input>
                <input type="submit" value="+"></input>
                </form>
            </div>
        )

    }
}