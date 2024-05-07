
function confirmDeleteCollege(button) {
    var collegeCode = button.getAttribute('college-code');
    var csrfToken = button.getAttribute('csrf-token');
    if (confirm("Are you sure you want to delete College " + collegeCode + " permanently?")) {
        fetch(`/college/delete_college/${collegeCode}`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log("Data received:", data);
            if (data === true) {
                console.log("Reloading the page...");
                window.location.reload();
            } else {
                window.location.reload();
                console.error("Error: " + (data ? data.message: "Data is undefined"));
            }
        });
    }
  }
  
  
function confirmDeleteCourse(button) {
    var course_code = button.getAttribute('course-code');
    var csrfToken = button.getAttribute('csrf-token');
    if (confirm("Are you sure you want to delete Course " + course_code + " permanently?")) {
        fetch(`/delete_course/${course_code}`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log("Data received:", data);
            if (data.success === true) {
                console.log("Reloading the page...");
                window.location.reload();
            } else {
                window.location.reload();
                console.error("Error: " + data.message);
            }
        });
    }
}
  
  
function confirmDeleteStudent(button) {
    var student_id = button.getAttribute('student-id');
    var csrfToken = button.getAttribute('csrf-token');
    if (confirm("Are you sure you want to delete Student " + student_id + " permanently ?\n")) {
        fetch(`/delete_student/${student_id}`, { 
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken
            }
        }).then(response => response.json())
        .then(data => {
            console.log("Data received:", data);
            if(data.success == true) {
            console.log("Reloading the page...");
            window.location.reload();
            } else {
            window.location.reload();
            console.error("Error: " + data.message);
            }
        });
    }
}
        
  