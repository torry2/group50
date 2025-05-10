document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('share-form').addEventListener('submit', function(event) {
      event.preventDefault();
      console.log('Form submitted');
      
      const formData = new FormData(this);
      console.log('Form data:');
      for (let [key, value] of formData.entries()) {
        console.log(key, value);
      }
      
      const submitBtn = this.querySelector('button[type="submit"]');
      const originalBtnText = submitBtn.innerHTML;
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Sharing...';
      
      fetch('/api/share', {
        method: 'POST',
        body: formData
      })
      .then(response => {
        console.log('Response status:', response.status);
        if (!response.ok) {
          throw new Error('Response not OK: ' + response.status);
        }
        return response.json();
      })
      .then(data => {
        console.log('Success:', data);
        
        alert('Share successful: ' + data.message);
        
        this.reset();
        
        const urlParams = new URLSearchParams(window.location.search);
        const goalParam = urlParams.get('goal');
        if (goalParam) {
          const goalCheckbox = document.getElementById(`share_goal${goalParam}`);
          if (goalCheckbox) {
            goalCheckbox.checked = true;
          }
        }
        
        fetchAndDisplaySharedGoals();
        
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnText;
      })
      .catch(error => {
        console.error('Error:', error);
        alert('Error sharing: ' + error);
        
        // Reset button
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnText;
      });
    });
    
    
    function fetchAndDisplaySharedGoals() {
      fetch('/api/share/list')
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') {
            const sharedGoalsAlerts = document.getElementById('shared-goals-alerts');
            sharedGoalsAlerts.innerHTML = '';
            
            
            if (data.shared_with_me && data.shared_with_me.length > 0) {
            
              data.shared_with_me.forEach(share => {
                const alertDiv = document.createElement('div');
                alertDiv.className = 'alert alert-info d-flex justify-content-between align-items-center mb-3';
                alertDiv.innerHTML = `
                  <div>
                    <strong>${share.owner_username}</strong> has shared their saving goals with you.
                    ${share.message ? `<p class="mb-0 mt-2 fst-italic">"${share.message}"</p>` : ''}
                  </div>
                  <button class="btn btn-primary btn-sm view-shared-goal" data-share-id="${share.id}">
                    View Goals
                  </button>
                `;
                sharedGoalsAlerts.appendChild(alertDiv);
              });
              
              // Add event listeners to view buttons
              document.querySelectorAll('.view-shared-goal').forEach(button => {
                button.addEventListener('click', function() {
                  const shareId = this.getAttribute('data-share-id');
                  viewSharedGoal(shareId);
                });
              });
            } else {
              // No shares
              sharedGoalsAlerts.innerHTML = '<div class="alert alert-secondary">No one has shared their goals with you yet.</div>';
            }
          } else {
            console.error('Error fetching shares:', data.message);
            sharedGoalsAlerts.innerHTML = '<div class="alert alert-danger">Error loading shared goals.</div>';
          }
        })
        .catch(error => {
          console.error('Error fetching shares:', error);
          const sharedGoalsAlerts = document.getElementById('shared-goals-alerts');
          sharedGoalsAlerts.innerHTML = '<div class="alert alert-danger">Error loading shared goals.</div>';
        });
    }
    
    
    function viewSharedGoal(shareId) {
      fetch(`/api/share/view/${shareId}`)
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') {
            // Populate modal with share data
            document.getElementById('shared-by-username').textContent = data.share.owner_username;
            document.getElementById('shared-date').textContent = data.share.share_date;
            
            // Check if there's a message
            const messageSection = document.getElementById('shared-message-container');
            if (data.share.message) {
              document.getElementById('shared-message').textContent = data.share.message;
              messageSection.style.display = 'block';
            } else {
              messageSection.style.display = 'none';
            }
            
            // Display goals
            const goalsContainer = document.getElementById('shared-goals-container');
            goalsContainer.innerHTML = '';
            
            if (data.goals && data.goals.length > 0) {
              data.goals.forEach(goal => {
                const goalDiv = document.createElement('div');
                goalDiv.className = 'mb-4';
                goalDiv.innerHTML = `
                  <h5>Goal ${goal.id}</h5>
                  <div class="d-flex justify-content-between mb-2">
                    <span>Progress: ${goal.progress}%</span>
                    <span>$${goal.amount.toFixed(2)} / $${goal.target.toFixed(2)}</span>
                  </div>
                  <div class="progress">
                    <div class="progress-bar bg-success" role="progressbar" style="width: ${goal.progress}%" 
                         aria-valuenow="${goal.progress}" aria-valuemin="0" aria-valuemax="100"></div>
                  </div>
                `;
                goalsContainer.appendChild(goalDiv);
              });
            } else {
              goalsContainer.innerHTML = '<div class="alert alert-warning">No goals found.</div>';
            }
            
            // Show the modal
            const modal = new bootstrap.Modal(document.getElementById('viewSharedGoalModal'));
            modal.show();
          } else {
            console.error('Error fetching shared goal:', data.message);
            alert('Error loading shared goal details.');
          }
        })
        .catch(error => {
          console.error('Error fetching shared goal:', error);
          alert('Error loading shared goal details.');
        });
    }
    
    // Initialize page by fetching shared goals
    fetchAndDisplaySharedGoals();
    
    // Check if there's a goal parameter in the URL and set the appropriate checkbox
    const urlParams = new URLSearchParams(window.location.search);
    const goalParam = urlParams.get('goal');
    if (goalParam) {
      // Uncheck all goals first
      document.getElementById('share_goal1').checked = false;
      document.getElementById('share_goal2').checked = false;
      document.getElementById('share_goal3').checked = false;
      
      // Check the specified goal
      const goalCheckbox = document.getElementById(`share_goal${goalParam}`);
      if (goalCheckbox) {
        goalCheckbox.checked = true;
      }
    }
  });