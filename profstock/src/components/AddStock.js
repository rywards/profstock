import React from 'react';
import axios from 'axios';

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
        axios.post(`https://jsonplaceholder.typicode.com/users`, { user })
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