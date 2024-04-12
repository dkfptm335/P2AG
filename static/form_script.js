const signupCheckbox = document.getElementById('signupCheckbox');
const signupSubChecklist = document.getElementById('signupSubChecklist');
const signupCheckbox2 = document.getElementById('signupCheckbox2');
const signupSub2Checklist = document.getElementById('signupSub2Checklist');
const signupCheckbox3 = document.getElementById('signupCheckbox3');
const signupSub3Checklist = document.getElementById('signupSub3Checklist');
const verificationCheckbox = document.getElementById('verificationCheckbox');
const verificationSubChecklist = document.getElementById('verificationSubChecklist');

signupCheckbox.addEventListener('change', function() {
    if (this.checked) {
        signupSubChecklist.style.display = 'block';
    } else {
        signupSubChecklist.style.display = 'none';
    }
});
signupCheckbox2.addEventListener('change', function() {
    if (this.checked) {
        signupSub2Checklist.style.display = 'block';
    } else {
        signupSub2Checklist.style.display = 'none';
    }
});
signupCheckbox3.addEventListener('change', function() {
    if (this.checked) {
        signupSub3Checklist.style.display = 'block';
    } else {
        signupSub3Checklist.style.display = 'none';
    }
});

verificationCheckbox.addEventListener('change', function() {
    if (this.checked) {
        verificationSubChecklist.style.display = 'block';
    } else {
        verificationSubChecklist.style.display = 'none';
    }
});