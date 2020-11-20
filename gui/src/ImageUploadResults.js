import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import history from './history';
import axios from 'axios';

const useStyles = makeStyles((theme) => ({
  root: {
    '& > *': {
      margin: theme.spacing(1),
    },
  },
  input: {
    display: 'none',
  },
}));

const ImageThumb = ({ image }) => {
  return <img src={URL.createObjectURL(image)} alt={image.name} />;
};

export default function UploadButtons() {
  
  const classes = useStyles();

  const [file, setFile] = React.useState("");

  function handleUpload(event) {
    setFile(event.target.files[0]);

    handleSubmit(event)
  }

  function handleSubmit(event) {
    event.preventDefault();
    let image_data = new FormData();
    image_data.append('image', setFile);
    let url = 'http://0.0.0.0:8080/';

    axios.post(url, image_data)
      .then(response => {
        console.log(response.data);
      })
      .catch(error => console.log(error))
  };

  return (
    <Grid container spacing={2} justify="center">
    <div className={classes.root}>
    <Button 
                  variant="contained" 
                  color="primary" 
                  onClick={() => history.push('/')}>
                Back
              </Button>
      <form>
        <br/><br/>
            <br/><br/>
            <header><h1>Image Recog</h1></header>
            
            
            <br/>
      <input type="file" onChange={handleUpload} />
      {file && <ImageThumb image={file} />}
      <imput type="submit"/>
      </form>
    </div>
    </Grid>
  );
}