// function parameters_SetEvents() {

//   const minusBtn = document.getElementsByClassName("minusBtn");
//   const plusBtn = document.getElementsByClassName("plusBtn");
//   const inputBox = document.getElementsByClassName("inputBox");

//   updateButtonStates();
//   minusBtn.addEventListener("click", decreaseValue);
//   plusBtn.addEventListener("click", increaseValue);
//   inputBox.addEventListener("input", handleQuantityChange);

// }

// function parameters_DelEvents() {

//   minusBtn.removeEventListener("click", decreaseValue);
//   plusBtn.removeEventListener("click", increaseValue);
//   inputBox.removeEventListener("input", handleQuantityChange);
// }
     
// function updateButtonStates() {
//   console.log("updateButtonStates");
//     const value = parseInt(inputBox.value);
//     minusBtn.disabled = value <= 1;
//     plusBtn.disabled = value >= parseInt(inputBox.max);
// }

// function decreaseValue() {
//   updateButtonStates();
//   console.log("decreaseValue");
//     let value = parseInt(inputBox.value);
//     value = isNaN(value) ? 1 : Math.max(value - 1, 1);
//     inputBox.value = value;
//     updateButtonStates();
//     handleQuantityChange();
// }
  
// function increaseValue() {
//   updateButtonStates();
//   console.log("increaseValue");
//     let value = parseInt(inputBox.value);
//     value = isNaN(value) ? 1 : Math.min(value + 1, parseInt(inputBox.max));
//     inputBox.value = value;
//     updateButtonStates();
//     handleQuantityChange();
// }
  
// function handleQuantityChange() {
//   console.log("QTYChange");
//     let value = parseInt(inputBox.value);
//     value = isNaN(value) ? 1 : value;
//     console.log("Quantity changed:", value);
// }


function parameters_SetEvents() {
  const minusBtns = document.querySelectorAll(".minus");
  const plusBtns = document.querySelectorAll(".plus");
  const inputBoxes = document.querySelectorAll(".input-box");
 
  updateButtonStates();
 
  minusBtns.forEach(btn => btn.addEventListener("click", decreaseValue));
  plusBtns.forEach(btn => btn.addEventListener("click", increaseValue));
  inputBoxes.forEach(box => box.addEventListener("input", handleQuantityChange));
 }
 
 function parameters_DelEvents() {
  const minusBtns = document.querySelectorAll(".minus");
  const plusBtns = document.querySelectorAll(".plus");
  const inputBoxes = document.querySelectorAll(".input-box");
 
  minusBtns.forEach(btn => btn.removeEventListener("click", decreaseValue));
  plusBtns.forEach(btn => btn.removeEventListener("click", increaseValue));
  inputBoxes.forEach(box => box.removeEventListener("input", handleQuantityChange));
 }
 
 function updateButtonStates() {
  document.querySelectorAll(".input-box").forEach(inputBox => {
     const value = parseInt(inputBox.value);
     const minusBtn = inputBox.parentNode.querySelector(".minus");
     const plusBtn = inputBox.parentNode.querySelector(".plus");
     minusBtn.disabled = value <= 1;
     plusBtn.disabled = value >= parseInt(inputBox.max);
  });
 }
 
 function decreaseValue() {
  const inputBox = this.parentNode.querySelector(".input-box");
  let value = parseInt(inputBox.value);
  value = isNaN(value) ? 1 : Math.max(value - 1, 1);
  inputBox.value = value;
  updateButtonStates();
  handleQuantityChange.call(inputBox);
 }
 
 function increaseValue() {
  const inputBox = this.parentNode.querySelector(".input-box");
  let value = parseInt(inputBox.value);
  value = isNaN(value) ? 1 : Math.min(value + 1, parseInt(inputBox.max));
  inputBox.value = value;
  updateButtonStates();
  handleQuantityChange.call(inputBox);
 }
 
 function handleQuantityChange() {
  const value = parseInt(this.value);
  console.log("Quantity changed:", value);
 }
