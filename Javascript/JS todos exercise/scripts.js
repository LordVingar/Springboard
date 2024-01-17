document.addEventListener('DOMContentLoaded', function() {
    const todoForm = document.getElementById('todoForm');
    const todoInput = document.getElementById('todoInput');
    const todoList = document.getElementById('todoList');

    // Load todos from localStorage
    const todos = JSON.parse(localStorage.getItem('todos')) || [];

    // Render existing todos
    renderTodos();

    // Event listener for adding a new todo
    todoForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const todoText = todoInput.value.trim();
        if (todoText !== '') {
            todos.push({ text: todoText, completed: false });
            saveTodos();
            renderTodos();
            todoInput.value = '';
        }
    });

    // Event listener for marking a todo as completed or removing it
    todoList.addEventListener('click', function(event) {
        const target = event.target;
        if (target.tagName === 'LI') {
            const index = target.dataset.index;
            todos[index].completed = !todos[index].completed;
            saveTodos();
            renderTodos();
        }
    });

    // Event listener for removing all completed todos
    document.getElementById('clearCompleted').addEventListener('click', function() {
        const completedTodos = todos.filter(todo => todo.completed);
        completedTodos.forEach(todo => {
            const index = todos.indexOf(todo);
            todos.splice(index, 1);
        });
        saveTodos();
        renderTodos();
    });

    // Function to render todos on the page
    function renderTodos() {
        todoList.innerHTML = '';
        
        todos.forEach((todo, index) => {
            const todoItem = document.createElement('li');
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.checked = todo.completed;
    
            // Event listener for checking/unchecking the checkbox
            checkbox.addEventListener('change', function() {
                todos[index].completed = !todos[index].completed;
                saveTodos();
                renderTodos();
            });
    
            const todoText = document.createElement('span');
            todoText.textContent = todo.text;
    
            // Add the checkbox and todo text to the li
            todoItem.appendChild(checkbox);
            todoItem.appendChild(todoText);
    
            todoItem.classList.toggle('completed', todo.completed);
            todoItem.dataset.index = index;
    
            todoList.appendChild(todoItem);
        });
    
        saveTodos();
    }

    // Function to save todos to localStorage
    function saveTodos() {
        localStorage.setItem('todos', JSON.stringify(todos));
    }
});