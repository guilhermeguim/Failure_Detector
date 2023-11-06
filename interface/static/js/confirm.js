function confirmDelete() {
  var confirmation = confirm("Are you sure you want to delete this register?");
  if (confirmation) {
    var password = prompt("Please enter your password:");
    if (password === "admin000") {
      return true;
    } else {
      alert("Password Incorrect");
      return false;
    }
  } else {
    alert("Canceled");
    return false;
  }
}

function confirmChange() {
    var confirmation = confirm("Are you sure you want to change this configs?");
    if (confirmation) {
      var password = prompt("Please enter your password:");
      if (password === "admin000") {
        return true;
      } else {
        alert("Password Incorrect");
        return false;
      }
    } else {
      alert("Canceled");
      return false;
    }
  }

function confirmRunTraining(){
  var confirmation = confirm("Running the training will stop the analysis from running. Are you sure you want to continue?");
    if (confirmation) {
      var password = prompt("Please enter your password:");
      if (password === "admin000") {
        return true;
      } else {
        alert("Password Incorrect");
        return false;
      }
    } else {
      alert("Canceled");
      return false;
    }
}

function confirmRunAnalisys(){
  var confirmation = confirm("Running the Analisys will stop the training from running. Are you sure you want to continue?");
    if (confirmation) {
      var password = prompt("Please enter your password:");
      if (password === "admin000") {
        return true;
      } else {
        alert("Password Incorrect");
        return false;
      }
    } else {
      alert("Canceled");
      return false;
    }
}

function confirmStop(){
  var confirmation = confirm("Are you sure you want to continue?");
    if (confirmation) {
      var password = prompt("Please enter your password:");
      if (password === "admin000") {
        return true;
      } else {
        alert("Password Incorrect");
        return false;
      }
    } else {
      alert("Canceled");
      return false;
    }
}