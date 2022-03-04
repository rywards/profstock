//const ReactDOM = require("react-dom");
const e = React.createElement

const ListItem = props => {
    return e('li',{className:'list-item', onClick: props.onDelete},props.title);
}

class List extends React.Component {
    constructor() {
        super();
        this.state = {items: ['IBM', 'Netflix']};
    }

    addItemHandler() {
        this.setState((prevState) => {
            return {items: prevState.items.concat('Microsoft')};
        });
    }
    
    deleteItemHandler(text) {
        this.setState((prevState) => {
            return {items: prevState.items.filter(item=> {
                return item !== text;
            })};
        });
    }

    render() {
        return e('div', null, [
            e('ul',{key: 'stock-list'}, this.state.items.map(item => {
                return e(ListItem, {title: item, key: item, onDelete: this.deleteItemHandler.bind(this, item)});
            })),
            e('button', {key: 'stock-button', onClick: this.addItemHandler.bind(this)}, 'Add stock')
        ]);
    }
}

ReactDOM.render(e(List), document.getElementById("stock-list"));