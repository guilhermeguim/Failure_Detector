// Set the initial value of class_value to 1
var today = new Date();
var year = today.getFullYear();
var month = String(today.getMonth() + 1).padStart(2, '0');
var day = String(today.getDate()).padStart(2, '0');

var class_value = year + '-' + month + '-' + day;



// Set up an interval to call the update_values function every 5 seconds
var intervalID = setInterval(() => {
  update_values(class_value);
}, 500000);

// Store the current scroll position
var scrollTop = 0;

// Define the update_values function, which takes in the parameter Lclass_value
function update_values(Lclass_value) {

  // Store the current scroll position of the table
  scrollTop = $('#table-container').scrollTop();
  // Use jQuery to make a GET request to '/newdata' with the class_value parameter
  $.getJSON($SCRIPT_ROOT + '/newdata_manual_alarm', {class_value: Lclass_value}, function(data) {
    
    
    
    // Construct a table using the data returned from the server
    var table = '<div class="table-container" id="table-container">';
    table += '<table class="table table-dark table-striped table-hover table-bordered">';
      table += '<thead id="t_head">';
        table += '<tr>';
          table += '<th scope="col" class="text-center">TYPE</th>';
          table += '<th scope="col" class="text-center">DATE</th>';
          table += '<th scope="col" class="text-center">TIME</th>';
        table += '</tr>';
      table += '</thead>';
      table += '<tbody class="table-group-divider" id="table-body">';

    // Determine how many rows are needed to display the data
    var rows_needed = 11; // assuming each row is 40px high
    var num_rows = data.result.length;
    var empty_row = '<tr class="table-dark text-center">';
        empty_row += '<td class="table-dark text-center">-</td>';
        empty_row += '<td class="table-dark text-center">-</td>';
        empty_row += '<td class="table-dark text-center">-</td></tr>';

    // Loop through the data and add rows to the table
    if (num_rows <= rows_needed){
      for (var i = 0; i < rows_needed; i++) {
        if (i < num_rows) {
          table += '<tr class="table-dark text-center">';
          for (var j = 0; j < data.result[i].length; j++) {
            table += '<td class="table-dark text-center">' + data.result[i][j] + '</td>';
          }
          table += '</tr>';
        } else {
          table += empty_row;
        }
      }
    } else {
      for (var i = 0; i < data.result.length; i++) {
        table += '<tr class="table-dark">';
        for (var j = 0; j < data.result[i].length; j++) {
            table += '<td class="table-dark">' + data.result[i][j] + '</td>';
        }
        table += '</tr>';
    }
    }
    

    table += '</tbody></table></div>';

    // Replace the contents of the 'result' div with the new table
    $('#result').html(table);

    // Log the data to the console
    // Restore the scroll position of the table
    $('#table-container').scrollTop(scrollTop);
  });
};

// Define the go_btn function
function go_btn() {
  // Get the value of the class dropdown and update class_value
  class_value = $('#class-dropdown').val();
  // Call update_values with the new class_value
  update_values(class_value);
  // Log the class_value to the console
  console.log(class_value);
}

// Get the contents of the 'result' div and display them
document.getElementById("result").innerHTML;