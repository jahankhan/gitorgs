// import React from 'react';
// import ReactDOM from 'react-dom';
// import Root from './components/root';
console.log("linked");

document.addEventListener("DOMContentLoaded", () => {
  // const root = document.getElementById('root');
  // ReactDOM.render(<Root />, root);

  const submit = document.getElementById("submit-btn");
  submit.addEventListener("click", () => {
    // console.log("click");
    // console.log(document.getElementById("org-name").value);
    window.location.href = window.location.href + 'org/' + document.getElementById("org-name").value;;
  });
});
