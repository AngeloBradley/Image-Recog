import React, { Component } from 'react';
import {render} from 'react-dom';
import ReactDOM from 'react-dom'
import axios from 'axios';
import Gallery from 'react-grid-gallery';
import Button from '@material-ui/core/Button';

class Home extends React.Component {
  constructor(props) {
    super(props);
    this.state = { images: this.props.images };

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

      ReactDOM.render(<Gallery images={IMAGES}></Gallery>, document.getElementById('imageGallery'))
      
    });
    event.preventDefault();
  }

  render() {

    return (
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          // alignItems: "center"
        }}
      >
        <form onSubmit={this.handleSubmit}>
          
          <br/><br/>
            <br/><br/>
            <header><h1>Image Recog</h1></header>
            
            
            {/* <br/> */}
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
            
          
          {/* <label>
            Image Search
          <input type="text" value={this.state.value} onChange={this.handleChange} />
          </label>
          <input type="submit" value="Submit" onClick={this.handleSubmit}/> */}
        </form>
        <div id='imageGallery'></div>
      </div>

    );
  }
}

export default Home