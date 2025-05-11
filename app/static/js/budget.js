document.addEventListener('DOMContentLoaded', function() {

    // Load budget data and render budget view
    loadBudgetData();
});

function loadBudgetData() {
    fetch('/api/data/get-income-budget')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const budget = data.income_budget;
                
                // Update total budget display
                document.getElementById('total-budget').textContent = budget.income;
                
                // Create budget categories display
                updateCategoriesDisplay(budget);
                
                // Create pie chart
                createPieChart(budget);
                
                // Update goals display
                updateGoalsDisplay(budget);
            } else {
                alert('Error loading budget: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error loading budget data:', error);
            alert('Error loading budget data. Please try again later.');
        });
}

function updateCategoriesDisplay(budget) {
    const categoriesContainer = document.getElementById('budget-categories');
    categoriesContainer.innerHTML = '';
    
    const categories = [
        { name: 'Food', value: budget.food },
        { name: 'Rent', value: budget.rent },
        { name: 'Utilities', value: budget.utilities },
        { name: 'Shopping', value: budget.shopping },
        { name: 'Entertainment', value: budget.entertainment },
        { name: 'Other', value: budget.other }
    ];
    
    categories.forEach(category => {
        const categoryRow = document.createElement('div');
        categoryRow.className = 'category-row bg-dark text-white p-2 mb-2 rounded d-flex justify-content-between';
        categoryRow.innerHTML = `
            <div class="category-name">${category.name}</div>
            <div class="category-value">$${category.value}</div>
        `;
        categoriesContainer.appendChild(categoryRow);
    });
}

function createPieChart(budget) {
    const ctx = document.getElementById('budget-pie-chart').getContext('2d');
    
    // Get categories and amounts for chart
    const categories = ['Food', 'Rent', 'Utilities', 'Shopping', 'Entertainment', 'Other'];
    const amounts = [
        parseFloat(budget.food) || 0,
        parseFloat(budget.rent) || 0, 
        parseFloat(budget.utilities) || 0,
        parseFloat(budget.shopping) || 0,
        parseFloat(budget.entertainment) || 0,
        parseFloat(budget.other) || 0
    ];
    
    // Filter out zero values
    const filteredCategories = [];
    const filteredAmounts = [];
    
    for (let i = 0; i < categories.length; i++) {
        if (amounts[i] > 0) {
            filteredCategories.push(categories[i]);
            filteredAmounts.push(amounts[i]);
        }
    }
    
    // Create chart
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: filteredCategories,
            datasets: [{
                data: filteredAmounts,
                backgroundColor: [
                    '#FF6384', 
                    '#36A2EB', 
                    '#FFCE56', 
                    '#4BC0C0', 
                    '#9966FF', 
                    '#FF9F40'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

function updateGoalsDisplay(budget) {
    const goalsContainer = document.getElementById('goals-container');
    goalsContainer.innerHTML = '';
    
    // Fetch transactions for goals
    fetch('/api/data/get-transactions')
        .then(response => response.json())
        .then(transactionData => {

          console.log("Transaction data response:", transactionData);

            if (transactionData.status === 'success') {
                // Calculate goal progress based on transactions
                const transactions = transactionData.transactions || [];
                
                console.log(`Found ${transactions.length} transactions`);
                transactions.forEach((transaction, index) => {
                console.log(`Transaction ${index + 1}:`, {
                    id: transaction.id,
                    name: transaction.name,
                    category: transaction.category,
                    amount: transaction.amount
                  });
                }); 



                // Calculate accumulated amounts for each goal

                const goalAmounts = {
                    goal1: 0,
                    goal2: 0,
                    goal3: 0
                };
                
                // Sum up transactions for each goal
                transactions.forEach(transaction => {
                    // Check if the transaction category is one of our goals
                    if (transaction.category === 'Goal 1') {
                        goalAmounts.goal1 += parseFloat(transaction.amount) || 0;
                    } else if (transaction.category === 'Goal 2') {
                        goalAmounts.goal2 += parseFloat(transaction.amount) || 0;
                    } else if (transaction.category === 'Goal 3') {
                        goalAmounts.goal3 += parseFloat(transaction.amount) || 0;
                    }
                });
                
                // Create goals array with correct target and amount values
                const goals = [
                    { 
                        id: 1, 
                        amount: goalAmounts.goal1, 
                        target: parseFloat(budget.goal1) || 100  // Use budget.goal1 as target, default to 100
                    },
                    { 
                        id: 2, 
                        amount: goalAmounts.goal2, 
                        target: parseFloat(budget.goal2) || 100
                    },
                    { 
                        id: 3, 
                        amount: goalAmounts.goal3, 
                        target: parseFloat(budget.goal3) || 100
                    }
                ];
                
                // Display each goal
                goals.forEach(goal => {
                    // Calculate progress percentage
                    const progress = goal.target > 0 ? 
                        Math.min(100, Math.round((goal.amount / goal.target) * 100)) : 0;
                    
                    const goalElement = document.createElement('div');
                    goalElement.className = 'goal-container mb-4';
                    goalElement.innerHTML = `
                        <div class="goal-header bg-dark text-white p-2 rounded d-flex justify-content-between align-items-center mb-2">
                            <div class="goal-progress-text">${goal.amount.toFixed(2)}/${goal.target.toFixed(2)} (${progress}%)</div>
                            <button class="share-button border-white" data-goal-id="${goal.id}" data-progress="${progress}">SHARE</button>
                        </div>
                        <div class="progress-container bg-dark rounded" style="height: 30px;">
                            <div class="progress-bar bg-white" style="width: ${progress}%; height: 100%;"></div>
                        </div>
                    `;
                    goalsContainer.appendChild(goalElement);
                });
                
                // Add event listeners to share buttons
                document.querySelectorAll('.share-button').forEach(button => {
                    button.addEventListener('click', function() {
                        const goalId = this.getAttribute('data-goal-id');
                        const progress = this.getAttribute('data-progress');
                    });
                });
            } else {
                console.error('Error loading transactions:', transactionData.message);
                
                // Display goals with zero progress as fallback
                displayDefaultGoals(budget);
            }
        })
        .catch(error => {
            console.error('Error fetching transactions:', error);
            
            // Display goals with zero progress as fallback
            displayDefaultGoals(budget);
        });
}

function setupShareButtons() {
    document.querySelectorAll('.share-button').forEach(button => {
        // First remove the existing event listener
        const buttonClone = button.cloneNode(true);
        button.parentNode.replaceChild(buttonClone, button);
        
        // Add our new event listener
        buttonClone.addEventListener('click', function() {
            const goalId = this.getAttribute('data-goal-id');
            shareGoal(goalId);
        });
    });
}

/**
 * Share a specific goal
 */
function shareGoal(goalId) {
    // Redirect to the share page with the goal ID in the query parameter
    window.location.href = `/share?goal=${goalId}`;
}

// Override the existing alert-based event listeners after the page loads
document.addEventListener('DOMContentLoaded', function() {
    // Wait for the original event handlers to be set up
    setTimeout(function() {
        // Replace the alert-based share buttons with our share page redirect
        setupShareButtons();
    }, 1000); // Wait 1 second to ensure the original code has run
});