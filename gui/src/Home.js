import React, { Component } from 'react';
import {render} from 'react-dom';
import ReactDOM from 'react-dom'
import axios from 'axios';
import Gallery from 'react-grid-gallery';
import Button from '@material-ui/core/Button';

class Home extends React.Component { //changed Component to React.Component
  constructor(props) {
    super(props);
    this.state = { images: this.props.images }; //changed { value: '' } to { images: this.props.images }

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({ value: event.target.value });
  }

  handleSubmit(event) {
    console.log(typeof ({ "query": this.state.value }));
    var query = { "query": this.state.value };
    console.log(query)
    axios.post("http://localhost:8090/search", query).then(token => {
      console.log(token);
      console.log(token.data);
      const IMAGES = token.data;

console.log(IMAGES)

      ReactDOM.render(<Gallery images={IMAGES}></Gallery>, document.getElementById('root'))
      console.log(IMAGES)
    });
    event.preventDefault();
  }

  render() {

    return (
      <div
        style={{
          display: "flex",
          justifyContent: "center",
        }}
      >
        <form>
          
          <br/><br/>
            <br/><br/>
            <header><h1>Image Recog</h1></header>
            
            <input
              value={this.state.value}
              onChange={this.handleChange}
              placeholder="Enter an identifier"
            />
            <Button 
                variant="contained" 
                color="primary" 
                onClick={this.handleSubmit}
            >
              Submit
            </Button>
        </form>
        <div id="imageGallery"></div>
      </div>

    );
  }
}

export default Home