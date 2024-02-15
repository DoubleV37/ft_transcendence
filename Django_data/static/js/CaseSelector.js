function  caseSelector(content) {
  switch (content) {
    case 'HOME_PAGE':
      CreateEventListeners(events_Objects[content]);
      console.log('lauch home');
      break;
    case 'SIGN_IN':
      CreateEventListeners(events_Objects[content]);
      console.log('lauch signin');
      break;
    case 'signup':
      console.log('lauch home');
      break;
    default:
      console.log('Uh problem in caseSelector');
  }
}
