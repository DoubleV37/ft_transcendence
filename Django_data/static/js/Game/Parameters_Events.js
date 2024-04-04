function parameters_SetEvents() {
  const minusBtns = document.querySelectorAll(".minus");
  const plusBtns = document.querySelectorAll(".plus");
  const inputBoxes = document.querySelectorAll(".input-box");

  updateButtonStates();

  minusBtns.forEach((btn) => btn.addEventListener("click", decreaseValue));
  plusBtns.forEach((btn) => btn.addEventListener("click", increaseValue));
  inputBoxes.forEach((box) =>
    box.addEventListener("input", handleQuantityChange),
  );

  //let element = document.getElementById(elementId)
}

function parameters_DelEvents() {
  const minusBtns = document.querySelectorAll(".minus");
  const plusBtns = document.querySelectorAll(".plus");
  const inputBoxes = document.querySelectorAll(".input-box");

  minusBtns.forEach((btn) => btn.removeEventListener("click", decreaseValue));
  plusBtns.forEach((btn) => btn.removeEventListener("click", increaseValue));
  inputBoxes.forEach((box) =>
    box.removeEventListener("input", handleQuantityChange),
  );
}

function updateButtonStates() {
  document.querySelectorAll(".input-box").forEach((inputBox) => {
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
