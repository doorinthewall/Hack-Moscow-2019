import React from 'react';

function HomepageImage() {
  const url = 'https://upload.wikimedia.org/wikipedia/commons/2/23/Lake_mapourika_NZ.jpeg';
  return (
    <img src={url} style={{width: 650}} alt='Image of Golden Gate Bridge' />
  );
}

export default HomepageImage;