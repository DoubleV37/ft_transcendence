function  caseSelector(content) {
  switch (content) {
    case 'home':
      console.log('lauch home');
      break;
    case 'signin':
      CreateEventListeners(signin_Object);
      console.log('lauch signin');
      break;
    case 'signup':
      console.log('lauch home');
      break;
    default:
      console.log('Uh problem in caseSelector');
  }
}
