/**
 * TinkerProfiles UI Components
 * 
 * Provides user interface components for profile management including
 * profile selector, creation/edit modals, and management interfaces.
 * 
 * @version 1.0.0
 * @author TinkerTools Development Team
 * @license MIT
 * @requires tinker-profiles.js
 * @requires Bootstrap 5
 */

/**
 * Profile UI Manager - Handles all profile-related UI interactions
 */
class TinkerProfilesUI {
    constructor() {
        this.initialized = false;
        this.currentEditingProfileId = null;
        this.modals = {};
    }

    /**
     * Initialize the profile UI system
     */
    static init() {
        if (!TinkerProfilesUI.instance) {
            TinkerProfilesUI.instance = new TinkerProfilesUI();
        }

        const instance = TinkerProfilesUI.instance;
        if (instance.initialized) return;

        // Initialize UI components
        instance.createUIComponents();
        instance.bindEventListeners();
        instance.setupProfileEventListeners();
        instance.updateProfileSelector();

        instance.initialized = true;
        console.log('TinkerProfiles UI initialized');
    }

    /**
     * Get the singleton instance
     */
    static getInstance() {
        if (!TinkerProfilesUI.instance) {
            TinkerProfilesUI.init();
        }
        return TinkerProfilesUI.instance;
    }

    /**
     * Create UI components and inject them into the DOM
     */
    createUIComponents() {
        this.createProfileSelector();
        this.createProfileModal();
        this.createManagementModal();
        this.createNotificationSystem();
    }

    /**
     * Create and inject the profile selector component
     */
    createProfileSelector() {
        const selector = document.createElement('div');
        selector.className = 'profile-selector';
        selector.id = 'tinker-profile-selector';
        selector.innerHTML = `
            <div class="dropdown">
                <button class="btn btn-outline-secondary dropdown-toggle" type="button" 
                        id="profileDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                    <i class="fas fa-user me-2"></i>
                    <span id="active-profile-name">Select Character</span>
                </button>
                <ul class="dropdown-menu" id="profile-dropdown-menu" aria-labelledby="profileDropdown">
                    <!-- Populated dynamically -->
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item" href="#" id="create-profile-btn">
                        <i class="fas fa-plus me-2"></i>Create New Profile
                    </a></li>
                    <li><a class="dropdown-item" href="#" id="manage-profiles-btn">
                        <i class="fas fa-cog me-2"></i>Manage Profiles
                    </a></li>
                </ul>
            </div>
        `;

        // Find the best location to inject the selector
        // Look for the second navbar-nav (the right side one with the clock)
        const navbarNavs = document.querySelectorAll('.navbar .navbar-nav');
        const targetNavbar = navbarNavs.length > 1 ? navbarNavs[1] : navbarNavs[0];
        
        if (targetNavbar) {
            const li = document.createElement('li');
            li.className = 'nav-item';
            li.appendChild(selector);
            
            // Insert before the clock item if it exists, otherwise append
            const clockItem = targetNavbar.querySelector('li:has(#rk-clock)') ||
                             targetNavbar.querySelector('li:last-child');
            if (clockItem && targetNavbar === navbarNavs[1]) {
                targetNavbar.insertBefore(li, clockItem);
            } else {
                targetNavbar.appendChild(li);
            }
        } else {
            // Fallback: inject at the top of body
            document.body.insertBefore(selector, document.body.firstChild);
        }
    }

    /**
     * Create the profile creation/edit modal
     */
    createProfileModal() {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.id = 'profile-modal';
        modal.tabIndex = -1;
        modal.setAttribute('aria-labelledby', 'profile-modal-title');
        modal.setAttribute('aria-hidden', 'true');
        
        modal.innerHTML = `
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="profile-modal-title">
                            <i class="fas fa-user me-2"></i>
                            <span id="profile-modal-title-text">Create Character Profile</span>
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form id="profile-form" novalidate>
                            <div class="row mb-3">
                                <div class="col-md-6">
                                    <label for="character-name" class="form-label">Character Name *</label>
                                    <input type="text" class="form-control" id="character-name" required 
                                           placeholder="Enter character name" maxlength="32">
                                    <div class="invalid-feedback">
                                        Character name is required (1-32 characters, alphanumeric only)
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <label for="character-level" class="form-label">Level</label>
                                    <input type="number" class="form-control" id="character-level" 
                                           min="1" max="220" value="220">
                                    <div class="invalid-feedback">
                                        Level must be between 1 and 220
                                    </div>
                                </div>
                            </div>
                            
                            <div class="row mb-3">
                                <div class="col-md-4">
                                    <label for="character-profession" class="form-label">Profession *</label>
                                    <select class="form-select" id="character-profession" required>
                                        <option value="">Select Profession</option>
                                        <option value="Adventurer">Adventurer</option>
                                        <option value="Agent">Agent</option>
                                        <option value="Bureaucrat">Bureaucrat</option>
                                        <option value="Doctor">Doctor</option>
                                        <option value="Enforcer">Enforcer</option>
                                        <option value="Engineer">Engineer</option>
                                        <option value="Fixer">Fixer</option>
                                        <option value="Keeper">Keeper</option>
                                        <option value="Martial Artist">Martial Artist</option>
                                        <option value="Meta-Physicist">Meta-Physicist</option>
                                        <option value="Nanotechnician">Nanotechnician</option>
                                        <option value="Soldier">Soldier</option>
                                        <option value="Trader">Trader</option>
                                        <option value="Shade">Shade</option>
                                    </select>
                                    <div class="invalid-feedback">
                                        Please select a profession
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <label for="character-faction" class="form-label">Faction</label>
                                    <select class="form-select" id="character-faction">
                                        <option value="Neutral">Neutral</option>
                                        <option value="Omni">Omni</option>
                                        <option value="Clan">Clan</option>
                                    </select>
                                </div>
                                <div class="col-md-4">
                                    <label for="character-account" class="form-label">Account Type</label>
                                    <select class="form-select" id="character-account">
                                        <option value="Paid">Paid</option>
                                        <option value="Froob">Froob</option>
                                    </select>
                                </div>
                            </div>
                            
                            <div class="row mb-3">
                                <div class="col-md-6">
                                    <label for="character-expansion" class="form-label">Expansion Access</label>
                                    <select class="form-select" id="character-expansion">
                                        <option value="All">All Expansions</option>
                                        <option value="SL">Shadowlands Only</option>
                                        <option value="AI">Alien Invasion</option>
                                        <option value="LoX">Lost Eden</option>
                                    </select>
                                </div>
                            </div>
                            
                            <!-- Attributes (Collapsible) -->
                            <div class="accordion mb-3">
                                <div class="accordion-item">
                                    <h2 class="accordion-header" id="attributes-header">
                                        <button class="accordion-button collapsed" type="button" 
                                                data-bs-toggle="collapse" data-bs-target="#attributes-collapse"
                                                aria-expanded="false" aria-controls="attributes-collapse">
                                            <i class="fas fa-chart-bar me-2"></i>Attributes (Optional)
                                        </button>
                                    </h2>
                                    <div id="attributes-collapse" class="accordion-collapse collapse"
                                         aria-labelledby="attributes-header">
                                        <div class="accordion-body">
                                            <div class="row">
                                                <div class="col-md-4 mb-2">
                                                    <label for="attr-strength" class="form-label">Strength</label>
                                                    <input type="number" class="form-control" id="attr-strength" 
                                                           value="1000" min="0" max="9999">
                                                </div>
                                                <div class="col-md-4 mb-2">
                                                    <label for="attr-stamina" class="form-label">Stamina</label>
                                                    <input type="number" class="form-control" id="attr-stamina" 
                                                           value="1000" min="0" max="9999">
                                                </div>
                                                <div class="col-md-4 mb-2">
                                                    <label for="attr-agility" class="form-label">Agility</label>
                                                    <input type="number" class="form-control" id="attr-agility" 
                                                           value="1000" min="0" max="9999">
                                                </div>
                                                <div class="col-md-4 mb-2">
                                                    <label for="attr-intelligence" class="form-label">Intelligence</label>
                                                    <input type="number" class="form-control" id="attr-intelligence" 
                                                           value="1000" min="0" max="9999">
                                                </div>
                                                <div class="col-md-4 mb-2">
                                                    <label for="attr-sense" class="form-label">Sense</label>
                                                    <input type="number" class="form-control" id="attr-sense" 
                                                           value="1000" min="0" max="9999">
                                                </div>
                                                <div class="col-md-4 mb-2">
                                                    <label for="attr-psychic" class="form-label">Psychic</label>
                                                    <input type="number" class="form-control" id="attr-psychic" 
                                                           value="1000" min="0" max="9999">
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-primary" id="save-profile-btn">
                            <span id="save-profile-text">Save Profile</span>
                            <span id="save-profile-spinner" class="spinner-border spinner-border-sm ms-2 d-none" 
                                  role="status" aria-hidden="true"></span>
                        </button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        this.modals.profile = new bootstrap.Modal(modal);
    }

    /**
     * Create the profile management modal
     */
    createManagementModal() {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.id = 'profile-management-modal';
        modal.tabIndex = -1;
        modal.setAttribute('aria-labelledby', 'management-modal-title');
        modal.setAttribute('aria-hidden', 'true');
        
        modal.innerHTML = `
            <div class="modal-dialog modal-xl">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="management-modal-title">
                            <i class="fas fa-users me-2"></i>Manage Character Profiles
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="table-responsive">
                            <table class="table table-striped table-hover" id="profiles-table">
                                <thead class="table-dark">
                                    <tr>
                                        <th>Character</th>
                                        <th>Profession</th>
                                        <th>Level</th>
                                        <th>Created</th>
                                        <th>Modified</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody id="profiles-table-body">
                                    <!-- Populated dynamically -->
                                </tbody>
                            </table>
                        </div>
                        
                        <!-- Import/Export Section -->
                        <div class="border-top pt-3 mt-3">
                            <h6><i class="fas fa-exchange-alt me-2"></i>Import/Export Profiles</h6>
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="import-file" class="form-label">Import Profiles</label>
                                        <input type="file" class="form-control" id="import-file" accept=".json">
                                        <div class="form-text">Import character profiles from JSON file</div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">Export Profiles</label>
                                        <div class="d-flex gap-2">
                                            <button type="button" class="btn btn-outline-primary" id="export-all-btn">
                                                <i class="fas fa-download me-1"></i>Export All
                                            </button>
                                            <button type="button" class="btn btn-outline-secondary" id="export-active-btn">
                                                <i class="fas fa-download me-1"></i>Export Active
                                            </button>
                                        </div>
                                        <div class="form-text">Download profiles as JSON file</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <div class="me-auto">
                            <small class="text-muted" id="storage-usage">Storage: 0KB used</small>
                        </div>
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        this.modals.management = new bootstrap.Modal(modal);
    }

    /**
     * Create notification system for user feedback
     */
    createNotificationSystem() {
        const container = document.createElement('div');
        container.className = 'position-fixed top-0 end-0 p-3';
        container.style.zIndex = '1055';
        container.id = 'tinker-notifications';
        document.body.appendChild(container);
    }

    /**
     * Bind event listeners for UI interactions
     */
    bindEventListeners() {
        // Profile selector events
        document.getElementById('create-profile-btn')?.addEventListener('click', (e) => {
            e.preventDefault();
            this.showCreateProfileModal();
        });

        document.getElementById('manage-profiles-btn')?.addEventListener('click', (e) => {
            e.preventDefault();
            this.showManagementModal();
        });

        // Profile form submission
        document.getElementById('save-profile-btn')?.addEventListener('click', (e) => {
            e.preventDefault();
            this.handleProfileSave();
        });

        // Import/Export events
        document.getElementById('import-file')?.addEventListener('change', (e) => {
            this.handleFileImport(e);
        });

        document.getElementById('export-all-btn')?.addEventListener('click', (e) => {
            e.preventDefault();
            this.exportAllProfiles();
        });

        document.getElementById('export-active-btn')?.addEventListener('click', (e) => {
            e.preventDefault();
            this.exportActiveProfile();
        });

        // Form validation
        const form = document.getElementById('profile-form');
        form?.addEventListener('input', () => {
            this.validateForm();
        });
    }

    /**
     * Setup profile event listeners
     */
    setupProfileEventListeners() {
        TinkerProfiles.addEventListener(PROFILE_EVENTS.PROFILE_CREATED, () => {
            this.updateProfileSelector();
        });

        TinkerProfiles.addEventListener(PROFILE_EVENTS.PROFILE_UPDATED, () => {
            this.updateProfileSelector();
        });

        TinkerProfiles.addEventListener(PROFILE_EVENTS.PROFILE_DELETED, () => {
            this.updateProfileSelector();
        });

        TinkerProfiles.addEventListener(PROFILE_EVENTS.ACTIVE_CHANGED, (event) => {
            this.updateActiveProfileDisplay(event.detail.profile);
        });
    }

    /**
     * Update the profile selector dropdown
     */
    updateProfileSelector() {
        const menu = document.getElementById('profile-dropdown-menu');
        const activeProfileName = document.getElementById('active-profile-name');
        
        if (!menu || !activeProfileName) return;

        const profiles = TinkerProfiles.getProfileList();
        const activeProfileId = TinkerProfiles.getActiveProfileId();
        const activeProfile = activeProfileId ? TinkerProfiles.getProfile(activeProfileId) : null;

        // Update active profile name
        if (activeProfile) {
            activeProfileName.textContent = `${activeProfile.character.name} (${activeProfile.character.profession})`;
        } else {
            activeProfileName.textContent = 'Select Character';
        }

        // Clear existing profile items (keep divider and management buttons)
        const existingItems = menu.querySelectorAll('.profile-item');
        existingItems.forEach(item => item.remove());

        // Add profile items
        const divider = menu.querySelector('.dropdown-divider');
        profiles.forEach(profile => {
            const li = document.createElement('li');
            li.className = 'profile-item';
            
            const a = document.createElement('a');
            a.className = 'dropdown-item';
            a.href = '#';
            a.dataset.profileId = profile.profileId;
            
            if (profile.profileId === activeProfileId) {
                a.classList.add('active');
            }
            
            a.innerHTML = `
                <div class="d-flex justify-content-between">
                    <span>${profile.name}</span>
                    <small class="text-muted">Lv${profile.level} ${this.abbreviateProfession(profile.profession)}</small>
                </div>
            `;
            
            a.addEventListener('click', (e) => {
                e.preventDefault();
                if (profile.profileId !== activeProfileId) {
                    this.switchToProfile(profile.profileId);
                }
            });
            
            li.appendChild(a);
            menu.insertBefore(li, divider);
        });

        // Show/hide based on profiles existence
        if (profiles.length === 0) {
            activeProfileName.textContent = 'No Profiles Created';
        }
    }

    /**
     * Abbreviate profession names for display
     */
    abbreviateProfession(profession) {
        const abbreviations = {
            'Adventurer': 'ADV',
            'Agent': 'AGE',
            'Bureaucrat': 'BUR',
            'Doctor': 'DOC',
            'Enforcer': 'ENF',
            'Engineer': 'ENG',
            'Fixer': 'FIX',
            'Keeper': 'KEE',
            'Martial Artist': 'MA',
            'Meta-Physicist': 'MP',
            'Nanotechnician': 'NT',
            'Soldier': 'SOL',
            'Trader': 'TRA',
            'Shade': 'SHA'
        };
        return abbreviations[profession] || profession.substring(0, 3).toUpperCase();
    }

    /**
     * Switch to a different profile
     */
    switchToProfile(profileId) {
        try {
            TinkerProfiles.setActiveProfile(profileId);
            this.showNotification('success', 'Profile switched successfully');
        } catch (error) {
            this.showNotification('error', `Failed to switch profile: ${error.message}`);
        }
    }

    /**
     * Show the create profile modal
     */
    showCreateProfileModal() {
        this.currentEditingProfileId = null;
        document.getElementById('profile-modal-title-text').textContent = 'Create Character Profile';
        document.getElementById('save-profile-text').textContent = 'Save Profile';
        this.resetProfileForm();
        this.modals.profile.show();
    }

    /**
     * Show the edit profile modal
     */
    showEditProfileModal(profileId) {
        const profile = TinkerProfiles.getProfile(profileId);
        if (!profile) {
            this.showNotification('error', 'Profile not found');
            return;
        }

        this.currentEditingProfileId = profileId;
        document.getElementById('profile-modal-title-text').textContent = 'Edit Character Profile';
        document.getElementById('save-profile-text').textContent = 'Update Profile';
        this.populateProfileForm(profile);
        this.modals.profile.show();
    }

    /**
     * Show the management modal
     */
    showManagementModal() {
        this.updateManagementTable();
        this.updateStorageUsage();
        this.modals.management.show();
    }

    /**
     * Reset the profile form to defaults
     */
    resetProfileForm() {
        const form = document.getElementById('profile-form');
        form.reset();
        form.classList.remove('was-validated');
        
        // Reset to defaults
        document.getElementById('character-level').value = '220';
        document.getElementById('character-faction').value = 'Neutral';
        document.getElementById('character-account').value = 'Paid';
        document.getElementById('character-expansion').value = 'All';
        
        // Reset attributes
        const attributes = ['strength', 'stamina', 'agility', 'intelligence', 'sense', 'psychic'];
        attributes.forEach(attr => {
            document.getElementById(`attr-${attr}`).value = '1000';
        });
    }

    /**
     * Populate the profile form with existing data
     */
    populateProfileForm(profile) {
        document.getElementById('character-name').value = profile.character.name || '';
        document.getElementById('character-level').value = profile.character.level || 220;
        document.getElementById('character-profession').value = profile.character.profession || '';
        document.getElementById('character-faction').value = profile.character.faction || 'Neutral';
        document.getElementById('character-account').value = profile.character.accountType || 'Paid';
        document.getElementById('character-expansion').value = profile.character.expansion || 'All';
        
        // Populate attributes
        if (profile.attributes) {
            document.getElementById('attr-strength').value = profile.attributes.strength || 1000;
            document.getElementById('attr-stamina').value = profile.attributes.stamina || 1000;
            document.getElementById('attr-agility').value = profile.attributes.agility || 1000;
            document.getElementById('attr-intelligence').value = profile.attributes.intelligence || 1000;
            document.getElementById('attr-sense').value = profile.attributes.sense || 1000;
            document.getElementById('attr-psychic').value = profile.attributes.psychic || 1000;
        }
    }

    /**
     * Validate the profile form
     */
    validateForm() {
        const form = document.getElementById('profile-form');
        const name = document.getElementById('character-name');
        const profession = document.getElementById('character-profession');
        const level = document.getElementById('character-level');
        
        let isValid = true;
        
        // Validate name
        if (!name.value.trim() || !/^[a-zA-Z][a-zA-Z0-9]*$/.test(name.value.trim())) {
            name.classList.add('is-invalid');
            isValid = false;
        } else {
            name.classList.remove('is-invalid');
            name.classList.add('is-valid');
        }
        
        // Validate profession
        if (!profession.value) {
            profession.classList.add('is-invalid');
            isValid = false;
        } else {
            profession.classList.remove('is-invalid');
            profession.classList.add('is-valid');
        }
        
        // Validate level
        const levelValue = parseInt(level.value);
        if (isNaN(levelValue) || levelValue < 1 || levelValue > 220) {
            level.classList.add('is-invalid');
            isValid = false;
        } else {
            level.classList.remove('is-invalid');
            level.classList.add('is-valid');
        }
        
        return isValid;
    }

    /**
     * Handle profile save (create or update)
     */
    async handleProfileSave() {
        if (!this.validateForm()) {
            document.getElementById('profile-form').classList.add('was-validated');
            return;
        }

        const saveBtn = document.getElementById('save-profile-btn');
        const saveText = document.getElementById('save-profile-text');
        const saveSpinner = document.getElementById('save-profile-spinner');
        
        // Show loading state
        saveBtn.disabled = true;
        saveSpinner.classList.remove('d-none');
        
        try {
            const profileData = this.getProfileDataFromForm();
            
            if (this.currentEditingProfileId) {
                // Update existing profile
                TinkerProfiles.updateProfile(this.currentEditingProfileId, profileData);
                this.showNotification('success', 'Profile updated successfully');
            } else {
                // Create new profile
                const profileId = TinkerProfiles.createProfile(profileData);
                TinkerProfiles.setActiveProfile(profileId);
                this.showNotification('success', 'Profile created successfully');
            }
            
            this.modals.profile.hide();
        } catch (error) {
            console.error('Profile save error:', error);
            if (error instanceof ProfileValidationError) {
                this.showNotification('error', `Validation error: ${error.validationErrors.join(', ')}`);
            } else {
                this.showNotification('error', `Failed to save profile: ${error.message}`);
            }
        } finally {
            // Reset loading state
            saveBtn.disabled = false;
            saveSpinner.classList.add('d-none');
        }
    }

    /**
     * Get profile data from form
     */
    getProfileDataFromForm() {
        return {
            character: {
                name: document.getElementById('character-name').value.trim(),
                profession: document.getElementById('character-profession').value,
                level: parseInt(document.getElementById('character-level').value),
                faction: document.getElementById('character-faction').value,
                expansion: document.getElementById('character-expansion').value,
                accountType: document.getElementById('character-account').value
            },
            attributes: {
                strength: parseInt(document.getElementById('attr-strength').value),
                stamina: parseInt(document.getElementById('attr-stamina').value),
                agility: parseInt(document.getElementById('attr-agility').value),
                intelligence: parseInt(document.getElementById('attr-intelligence').value),
                sense: parseInt(document.getElementById('attr-sense').value),
                psychic: parseInt(document.getElementById('attr-psychic').value)
            }
        };
    }

    /**
     * Update the management table
     */
    updateManagementTable() {
        const tbody = document.getElementById('profiles-table-body');
        if (!tbody) return;

        const profiles = TinkerProfiles.getProfileList();
        const activeProfileId = TinkerProfiles.getActiveProfileId();
        
        tbody.innerHTML = '';
        
        profiles.forEach(profile => {
            const row = document.createElement('tr');
            if (profile.profileId === activeProfileId) {
                row.classList.add('table-primary');
            }
            
            row.innerHTML = `
                <td>
                    <strong>${profile.name}</strong>
                    ${profile.profileId === activeProfileId ? '<span class="badge bg-primary ms-1">Active</span>' : ''}
                </td>
                <td>${profile.profession}</td>
                <td>${profile.level}</td>
                <td>${new Date(profile.created).toLocaleDateString()}</td>
                <td>${new Date(profile.modified).toLocaleDateString()}</td>
                <td>
                    <div class="btn-group btn-group-sm" role="group">
                        <button type="button" class="btn btn-outline-primary" data-action="edit" data-profile-id="${profile.profileId}" title="Edit">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button type="button" class="btn btn-outline-secondary" data-action="duplicate" data-profile-id="${profile.profileId}" title="Duplicate">
                            <i class="fas fa-copy"></i>
                        </button>
                        <button type="button" class="btn btn-outline-info" data-action="export" data-profile-id="${profile.profileId}" title="Export">
                            <i class="fas fa-download"></i>
                        </button>
                        <button type="button" class="btn btn-outline-danger" data-action="delete" data-profile-id="${profile.profileId}" title="Delete" 
                                ${profile.profileId === activeProfileId ? 'disabled' : ''}>
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </td>
            `;
            
            tbody.appendChild(row);
        });
        
        // Bind action buttons
        tbody.addEventListener('click', (e) => {
            const button = e.target.closest('button[data-action]');
            if (!button) return;
            
            const action = button.dataset.action;
            const profileId = button.dataset.profileId;
            
            this.handleManagementAction(action, profileId);
        });
    }

    /**
     * Handle management table actions
     */
    handleManagementAction(action, profileId) {
        switch (action) {
            case 'edit':
                this.modals.management.hide();
                setTimeout(() => this.showEditProfileModal(profileId), 300);
                break;
            case 'duplicate':
                this.duplicateProfile(profileId);
                break;
            case 'export':
                this.exportProfile(profileId);
                break;
            case 'delete':
                this.deleteProfile(profileId);
                break;
        }
    }

    /**
     * Duplicate a profile
     */
    duplicateProfile(profileId) {
        try {
            const profile = TinkerProfiles.getProfile(profileId);
            if (!profile) throw new Error('Profile not found');
            
            const duplicateData = { ...profile };
            duplicateData.character.name = `${profile.character.name} Copy`;
            delete duplicateData.meta; // Will be regenerated
            
            const newProfileId = TinkerProfiles.createProfile(duplicateData);
            this.showNotification('success', 'Profile duplicated successfully');
            this.updateManagementTable();
        } catch (error) {
            this.showNotification('error', `Failed to duplicate profile: ${error.message}`);
        }
    }

    /**
     * Delete a profile with confirmation
     */
    deleteProfile(profileId) {
        const profile = TinkerProfiles.getProfile(profileId);
        if (!profile) return;
        
        if (confirm(`Are you sure you want to delete the profile "${profile.character.name}"? This action cannot be undone.`)) {
            try {
                TinkerProfiles.deleteProfile(profileId);
                this.showNotification('success', 'Profile deleted successfully');
                this.updateManagementTable();
            } catch (error) {
                this.showNotification('error', `Failed to delete profile: ${error.message}`);
            }
        }
    }

    /**
     * Export a single profile
     */
    exportProfile(profileId) {
        try {
            const data = TinkerProfiles.exportProfile(profileId);
            const profile = TinkerProfiles.getProfile(profileId);
            const filename = `tinkertools-profile-${profile.character.name.toLowerCase().replace(/[^a-z0-9]/g, '-')}.json`;
            this.downloadFile(data, filename);
            this.showNotification('success', 'Profile exported successfully');
        } catch (error) {
            this.showNotification('error', `Failed to export profile: ${error.message}`);
        }
    }

    /**
     * Export all profiles
     */
    exportAllProfiles() {
        try {
            const data = TinkerProfiles.exportAllProfiles();
            const filename = `tinkertools-profiles-${new Date().toISOString().split('T')[0]}.json`;
            this.downloadFile(data, filename);
            this.showNotification('success', 'All profiles exported successfully');
        } catch (error) {
            this.showNotification('error', `Failed to export profiles: ${error.message}`);
        }
    }

    /**
     * Export active profile
     */
    exportActiveProfile() {
        const activeProfileId = TinkerProfiles.getActiveProfileId();
        if (!activeProfileId) {
            this.showNotification('warning', 'No active profile to export');
            return;
        }
        this.exportProfile(activeProfileId);
    }

    /**
     * Handle file import
     */
    handleFileImport(event) {
        const file = event.target.files[0];
        if (!file) return;
        
        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const data = e.target.result;
                
                // Try to parse and determine if single profile or multiple
                const parsed = JSON.parse(data);
                let importedIds = [];
                
                if (parsed.profiles && Array.isArray(parsed.profiles)) {
                    // Multiple profiles
                    importedIds = TinkerProfiles.importProfiles(data);
                } else {
                    // Single profile
                    importedIds = [TinkerProfiles.importProfile(data)];
                }
                
                this.showNotification('success', `Successfully imported ${importedIds.length} profile(s)`);
                this.updateManagementTable();
                
                // Clear the file input
                event.target.value = '';
            } catch (error) {
                this.showNotification('error', `Failed to import profile(s): ${error.message}`);
                event.target.value = '';
            }
        };
        
        reader.readAsText(file);
    }

    /**
     * Update storage usage display
     */
    updateStorageUsage() {
        const usage = TinkerProfiles.getStorageUsage();
        const element = document.getElementById('storage-usage');
        if (element) {
            const sizeKB = Math.round(usage.totalSize / 1024);
            const maxKB = Math.round(usage.maxSize / 1024);
            element.textContent = `Storage: ${sizeKB}KB / ${maxKB}KB used (${Math.round(usage.percentUsed)}%)`;
        }
    }

    /**
     * Update active profile display
     */
    updateActiveProfileDisplay(profile) {
        if (profile) {
            // Dispatch event for apps to react to profile change
            window.dispatchEvent(new CustomEvent('tinkerProfileChanged', {
                detail: { profile }
            }));
        }
    }

    /**
     * Show notification to user
     */
    showNotification(type, message, duration = 5000) {
        const container = document.getElementById('tinker-notifications');
        if (!container) return;
        
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${this.getBootstrapColor(type)} border-0`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');
        
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas ${this.getNotificationIcon(type)} me-2"></i>${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;
        
        container.appendChild(toast);
        
        const bsToast = new bootstrap.Toast(toast, {
            autohide: true,
            delay: duration
        });
        
        bsToast.show();
        
        // Remove from DOM after hiding
        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    }

    /**
     * Get Bootstrap color class for notification type
     */
    getBootstrapColor(type) {
        const colors = {
            success: 'success',
            error: 'danger',
            warning: 'warning',
            info: 'info'
        };
        return colors[type] || 'secondary';
    }

    /**
     * Get FontAwesome icon for notification type
     */
    getNotificationIcon(type) {
        const icons = {
            success: 'fa-check-circle',
            error: 'fa-exclamation-circle',
            warning: 'fa-exclamation-triangle',
            info: 'fa-info-circle'
        };
        return icons[type] || 'fa-bell';
    }

    /**
     * Download data as file
     */
    downloadFile(data, filename) {
        const blob = new Blob([data], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        link.style.display = 'none';
        
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        URL.revokeObjectURL(url);
    }
}

// Static instance property
TinkerProfilesUI.instance = null;

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { TinkerProfilesUI };
}

// Auto-initialize when DOM is ready
if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            // Wait a bit for TinkerProfiles to initialize first
            setTimeout(() => {
                TinkerProfilesUI.init();
            }, 100);
        });
    } else {
        setTimeout(() => {
            TinkerProfilesUI.init();
        }, 100);
    }
}