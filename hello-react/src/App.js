import React, {useEffect, useState, Component } from 'react';
// import logo from './logo.svg';
import './App.css';
import HomepageImage from './components/HomepageImage'
import { Locations, ButtonExamplePositive } from './components/LOCATIONS.js'
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.css';

// const formData = new FormData();
// formData.append('latitude', 55.819148);
// formData.append('longitude', 37.581053);
// '/get_recommendation?latitude=${encodeURIComponent(sendthis.lat)}&longitude=${encodeURIComponent(sendthis.long)'
const sendthis = {lat:55.819148, long:37.581053}


class App extends Component {

  constructor(props) {
    super(props);

    this.state = {
      isLoading: false,
      formData: {
        textfield1: '',
        textfield2: '',
        select1: 1,
        select2: 1,
        select3: 1
      },
      result: ""
    };
  }

  handlePredictClick = (event) => {
    fetch('/get_recommendation?latitude=55.819148&longitude=37.581053&n=3&cat_filters=petrol-station').then(response =>
     response.json().then(data => {
      this.setState({
          result: data
        });console.log(this.state.result)
      }
      )
     )
  }

  handleCancelClick = (event) => {
    this.setState({ result: "" });
  }

  render() {
    const result = this.state.result;

    return (
      <Container>
        <div>
          <h1 className="title">Some App</h1>
        </div>
        <div className="content">
          <Form>
            <Row>
              <Col>
                <div>
                  <Button
                    block
                    variant="success"
                    onClick={this.handlePredictClick}>
                    Find Me Places
                  </Button>
                   </div>
                  </Col>
                  <Col>
                    <Button
                      block
                      variant="danger"
                      onClick={this.handleCancelClick}>
                      Reset prediction
                    </Button>
                  </Col>
              </Row>          
            </Form>
          {result === "" ? null :
            (<Row>
              <Col>
                <Locations locations={result} /> 
              </Col>
            </Row>)
          }
        </div>
      </Container>
      );
     
  }

}

  

export default App;

// function App() {

//   // handlePredictClick = (event) => {
//   // const [locations, setLocations] = useState([]);
//   // useEffect(() => {
//   //   fetch('/get_recommendation?latitude=55.819148&longitude=37.581053&n=3').then(response =>
//   //    response.json().then(data => {
//   //     setLocations(data);
//   //     })
//   //   );
//   // }, []);
//   // }


//   const [locations, setLocations] = useState([]);
//   useEffect(() => {
//     fetch('/get_recommendation?latitude=55.819148&longitude=37.581053&n=3').then(response =>
//      response.json().then(data => {
//       setLocations(data);
//       })
//     );
//   }, []);

// console.log(locations)

//   // return (
//   //   <div className="App">
//   //     <header className="App-header">
//   //       <HomepageImage />
//   //       <p>
//   //         HUI!
//   //       </p>
//   //     </header>
//   //   </div>
//   // );
//   return (
//     <div className="App">
//       <Locations locations={locations} /> 
//       <ButtonExamplePositive />
//     </div>
//   );

// }

// export default App;
