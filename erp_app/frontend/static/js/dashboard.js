// Dashboard JavaScript

let currentModule = 'dashboard';
let dashboardData = {};
let charts = {};

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    checkAuthentication();
    setupEventListeners();
    loadDashboardData();
    loadUserInfo();
});

function checkAuthentication() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/login';
        return;
    }
    
    // Verify token is still valid
    verifyToken(token).then(valid => {
        if (!valid) {
            logout();
        }
    });
}

async function verifyToken(token) {
    try {
        const response = await fetch('/api/auth/me', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        return response.ok;
    } catch (error) {
        console.error('Token verification error:', error);
        return false;
    }
}

function setupEventListeners() {
    // Module navigation
    document.querySelectorAll('[data-module]').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const module = this.getAttribute('data-module');
            loadModule(module);
        });
    });
    
    // Dashboard link
    document.querySelector('a[href="/"]').addEventListener('click', function(e) {
        e.preventDefault();
        showDashboard();
    });
}

function loadUserInfo() {
    const userInfo = JSON.parse(localStorage.getItem('user_info') || '{}');
    const usernameElement = document.getElementById('username');
    if (usernameElement && userInfo.full_name) {
        usernameElement.textContent = userInfo.full_name;
    }
}

async function loadDashboardData() {
    try {
        showLoading('dashboard-content');
        
        const token = localStorage.getItem('access_token');
        const response = await fetch('/api/dashboard/stats', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            dashboardData = await response.json();
            updateDashboardStats();
            loadCharts();
            loadRecentActivities();
        } else {
            throw new Error('Failed to load dashboard data');
        }
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        showNotification('Error loading dashboard data', 'error');
    } finally {
        hideLoading('dashboard-content');
    }
}

function updateDashboardStats() {
    // Update stats cards
    document.getElementById('total-revenue').textContent = 
        `$${dashboardData.accounting?.total_revenue?.toLocaleString() || 0}`;
    
    document.getElementById('total-orders').textContent = 
        dashboardData.sales?.total_orders || 0;
    
    document.getElementById('total-customers').textContent = 
        dashboardData.accounting?.total_customers || 0;
    
    document.getElementById('total-employees').textContent = 
        dashboardData.hr?.total_employees || 0;
}

async function loadCharts() {
    try {
        const token = localStorage.getItem('access_token');
        
        // Load revenue chart data
        const revenueResponse = await fetch('/api/dashboard/charts/revenue', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (revenueResponse.ok) {
            const revenueData = await revenueResponse.json();
            createRevenueChart(revenueData);
        }
        
        // Load pipeline chart data
        const pipelineResponse = await fetch('/api/dashboard/charts/sales-pipeline', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (pipelineResponse.ok) {
            const pipelineData = await pipelineResponse.json();
            createPipelineChart(pipelineData);
        }
    } catch (error) {
        console.error('Error loading charts:', error);
    }
}

function createRevenueChart(data) {
    const ctx = document.getElementById('revenueChart').getContext('2d');
    
    if (charts.revenue) {
        charts.revenue.destroy();
    }
    
    charts.revenue = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels || [],
            datasets: [{
                label: 'Revenue',
                data: data.data || [],
                borderColor: '#4e73df',
                backgroundColor: 'rgba(78, 115, 223, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toLocaleString();
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

function createPipelineChart(data) {
    const ctx = document.getElementById('pipelineChart').getContext('2d');
    
    if (charts.pipeline) {
        charts.pipeline.destroy();
    }
    
    charts.pipeline = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.stages || [],
            datasets: [{
                data: data.values || [],
                backgroundColor: [
                    '#4e73df',
                    '#1cc88a',
                    '#36b9cc',
                    '#f6c23e',
                    '#e74a3b'
                ],
                borderWidth: 2
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

async function loadRecentActivities() {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch('/api/dashboard/recent-activities', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const activities = await response.json();
            displayRecentActivities(activities);
        }
    } catch (error) {
        console.error('Error loading recent activities:', error);
    }
}

function displayRecentActivities(activities) {
    const container = document.getElementById('recent-activities');
    
    if (activities.length === 0) {
        container.innerHTML = '<p class="text-muted text-center">No recent activities</p>';
        return;
    }
    
    const activitiesHtml = activities.map(activity => `
        <div class="activity-item">
            <div class="d-flex justify-content-between">
                <div>
                    <h6 class="mb-1">${activity.title}</h6>
                    <p class="mb-1 text-muted">${activity.description}</p>
                    <span class="badge bg-primary">${activity.module}</span>
                </div>
                <small class="activity-time">${formatDate(activity.timestamp)}</small>
            </div>
        </div>
    `).join('');
    
    container.innerHTML = activitiesHtml;
}

async function loadModule(moduleName) {
    try {
        currentModule = moduleName;
        updateNavigation(moduleName);
        
        document.getElementById('page-title').textContent = 
            moduleName.charAt(0).toUpperCase() + moduleName.slice(1);
        
        // Hide dashboard content, show module content
        document.getElementById('dashboard-content').style.display = 'none';
        document.getElementById('module-content').style.display = 'block';
        
        const moduleContainer = document.getElementById('module-data');
        showLoading('module-data');
        
        const token = localStorage.getItem('access_token');
        const response = await fetch(`/api/${moduleName}/${getModuleEndpoint(moduleName)}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            renderModuleData(moduleName, data);
        } else {
            throw new Error(`Failed to load ${moduleName} data`);
        }
    } catch (error) {
        console.error(`Error loading ${moduleName}:`, error);
        showNotification(`Error loading ${moduleName} data`, 'error');
    } finally {
        hideLoading('module-data');
    }
}

function getModuleEndpoint(moduleName) {
    const endpoints = {
        'crm': 'leads',
        'inventory': 'products',
        'accounting': 'invoices',
        'hr': 'employees',
        'sales': 'orders'
    };
    return endpoints[moduleName] || 'data';
}

function renderModuleData(moduleName, data) {
    const container = document.getElementById('module-data');
    
    const moduleConfig = {
        'crm': {
            title: 'Customer Relationship Management',
            data: data.leads || [],
            columns: ['ID', 'Name', 'Email', 'Company', 'Status', 'Created'],
            getRowData: (item) => [
                item.id,
                `${item.first_name} ${item.last_name}`,
                item.email || '-',
                item.company || '-',
                `<span class="badge bg-${getStatusColor(item.status)}">${item.status}</span>`,
                formatDate(item.created_at)
            ]
        },
        'inventory': {
            title: 'Inventory Management',
            data: data.products || [],
            columns: ['SKU', 'Name', 'Type', 'Price', 'Stock', 'Status'],
            getRowData: (item) => [
                item.sku,
                item.name,
                item.type,
                `$${item.selling_price}`,
                item.current_stock,
                `<span class="badge bg-${item.is_active ? 'success' : 'secondary'}">${item.is_active ? 'Active' : 'Inactive'}</span>`
            ]
        },
        'accounting': {
            title: 'Accounting & Finance',
            data: data.invoices || [],
            columns: ['Invoice #', 'Customer', 'Amount', 'Status', 'Due Date'],
            getRowData: (item) => [
                item.invoice_number,
                item.customer_id,
                `$${item.total_amount}`,
                `<span class="badge bg-${getStatusColor(item.status)}">${item.status}</span>`,
                formatDate(item.due_date)
            ]
        },
        'hr': {
            title: 'Human Resources',
            data: data.employees || [],
            columns: ['ID', 'Name', 'Email', 'Department', 'Hire Date', 'Status'],
            getRowData: (item) => [
                item.employee_id,
                `${item.first_name} ${item.last_name}`,
                item.email,
                item.department_id,
                formatDate(item.hire_date),
                `<span class="badge bg-${getStatusColor(item.status)}">${item.status}</span>`
            ]
        },
        'sales': {
            title: 'Sales Management',
            data: data.orders || [],
            columns: ['Order #', 'Customer', 'Amount', 'Status', 'Order Date'],
            getRowData: (item) => [
                item.order_number,
                item.customer_id,
                `$${item.total_amount}`,
                `<span class="badge bg-${getStatusColor(item.status)}">${item.status}</span>`,
                formatDate(item.order_date)
            ]
        }
    };
    
    const config = moduleConfig[moduleName];
    if (!config) {
        container.innerHTML = '<p class="text-center">Module configuration not found</p>';
        return;
    }
    
    const html = `
        <div class="module-header">
            <h3>${config.title}</h3>
            <div class="module-actions">
                <button class="btn btn-primary" onclick="showCreateModal('${moduleName}')">
                    <i class="fas fa-plus"></i> Add New
                </button>
                <button class="btn btn-outline-secondary" onclick="refreshModule('${moduleName}')">
                    <i class="fas fa-sync-alt"></i> Refresh
                </button>
            </div>
        </div>
        
        <div class="table-responsive">
            <table class="table table-hover">
                <thead>
                    <tr>
                        ${config.columns.map(col => `<th>${col}</th>`).join('')}
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${config.data.map(item => `
                        <tr>
                            ${config.getRowData(item).map(cell => `<td>${cell}</td>`).join('')}
                            <td>
                                <div class="action-buttons">
                                    <button class="btn btn-sm btn-outline-primary" onclick="viewItem('${moduleName}', ${item.id})">
                                        <i class="fas fa-eye"></i>
                                    </button>
                                    <button class="btn btn-sm btn-outline-secondary" onclick="editItem('${moduleName}', ${item.id})">
                                        <i class="fas fa-edit"></i>
                                    </button>
                                </div>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
        
        ${config.data.length === 0 ? '<p class="text-center text-muted">No data available</p>' : ''}
    `;
    
    container.innerHTML = html;
}

function showDashboard() {
    currentModule = 'dashboard';
    updateNavigation('dashboard');
    
    document.getElementById('page-title').textContent = 'Dashboard';
    document.getElementById('dashboard-content').style.display = 'block';
    document.getElementById('module-content').style.display = 'none';
    
    // Refresh dashboard data
    loadDashboardData();
}

function updateNavigation(activeModule) {
    // Remove active class from all nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    
    // Add active class to current module
    if (activeModule === 'dashboard') {
        document.querySelector('a[href="/"]').classList.add('active');
    } else {
        const moduleLink = document.querySelector(`[data-module="${activeModule}"]`);
        if (moduleLink) {
            moduleLink.classList.add('active');
        }
    }
}

function getStatusColor(status) {
    const colors = {
        'new': 'danger',
        'contacted': 'warning',
        'qualified': 'info',
        'converted': 'success',
        'active': 'success',
        'pending': 'warning',
        'confirmed': 'info',
        'completed': 'success',
        'paid': 'success',
        'draft': 'secondary',
        'sent': 'primary'
    };
    return colors[status] || 'secondary';
}

function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString();
}

function showLoading(elementId) {
    const element = document.getElementById(elementId);
    element.classList.add('loading');
}

function hideLoading(elementId) {
    const element = document.getElementById(elementId);
    element.classList.remove('loading');
}

function showNotification(message, type = 'info') {
    const toast = document.getElementById('notification-toast');
    const toastMessage = document.getElementById('toast-message');
    
    toastMessage.textContent = message;
    
    // Update toast styling based on type
    toast.className = `toast ${type === 'error' ? 'bg-danger text-white' : ''}`;
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
}

function refreshData() {
    if (currentModule === 'dashboard') {
        loadDashboardData();
    } else {
        loadModule(currentModule);
    }
}

function refreshModule(moduleName) {
    loadModule(moduleName);
}

function showCreateModal(moduleName) {
    showNotification(`Create ${moduleName} functionality not implemented in demo`, 'info');
}

function viewItem(moduleName, itemId) {
    showNotification(`View ${moduleName} item ${itemId} functionality not implemented in demo`, 'info');
}

function editItem(moduleName, itemId) {
    showNotification(`Edit ${moduleName} item ${itemId} functionality not implemented in demo`, 'info');
}

function showProfile() {
    showNotification('Profile functionality not implemented in demo', 'info');
}

function showSettings() {
    showNotification('Settings functionality not implemented in demo', 'info');
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_info');
    window.location.href = '/login';
}
