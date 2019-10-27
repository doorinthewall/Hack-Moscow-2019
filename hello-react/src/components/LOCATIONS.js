import React from 'react';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import { List, Header, Rating, Button } from "semantic-ui-react";

// export const Locations = ({ locations }) => {
// 	return <div>{locations.length}</div>;
// };

export const Locations = ({ locations }) => {
 return (
    <List>
      {locations.map(location => {
        return (
          <List.Item key={location.name}>
            <Header className="result-container">{location.name}</Header>
            	<Row className="address">
            	Address: 
            	{ location.address}
            	</Row> 
            	<Row className="address">
            	Info:
            	{ location.open}
            	</Row> 
          </List.Item>
        );
      })}
    </List>
  );
};


export const ButtonExamplePositive = () => (
  <div>
    <Button positive>Find Me Places</Button>
  </div>
)
