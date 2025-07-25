/**
 * TinkerProfiles - Core Character Profile Management API
 * 
 * Provides centralized access to character profile data across all TinkerTools applications.
 * Uses LocalStorage for client-side data persistence with complete user privacy.
 * 
 * @version 1.0.0
 * @author TinkerTools Development Team
 * @license MIT
 */

// Global constants and configuration
const TINKER_PROFILES_CONFIG = {
    version: '1.0.0',
    schemaVersion: '1.0',
    storageKeys: {
        profilesMeta: 'tinkertools.profiles.meta',
        activeProfile: 'tinkertools.profiles.active',
        profilePrefix: 'tinkertools.profile.',
        schema: 'tinkertools.cache.schema',
        settings: 'tinkertools.cache.settings'
    },
    storage: {
        maxProfiles: 50,
        maxProfileSize: 51200, // 50KB
        cacheTimeout: 300000,  // 5 minutes
        batchDelay: 100        // 100ms
    },
    professions: [
        'Adventurer', 'Agent', 'Bureaucrat', 'Doctor', 'Enforcer', 'Engineer',
        'Fixer', 'Keeper', 'Martial Artist', 'Meta-Physicist', 'Nanotechnician',
        'Soldier', 'Trader', 'Shade'
    ]
};

// Event types for profile system
const PROFILE_EVENTS = {
    PROFILE_CREATED: 'profile:created',
    PROFILE_UPDATED: 'profile:updated',
    PROFILE_DELETED: 'profile:deleted',
    ACTIVE_CHANGED: 'profile:active:changed',
    APP_DATA_UPDATED: 'profile:appdata:updated',
    STORAGE_ERROR: 'profile:storage:error',
    VALIDATION_ERROR: 'profile:validation:error'
};

/**
 * Custom error classes for profile system
 */
class ProfileStorageError extends Error {
    constructor(message, code, originalError = null) {
        super(message);
        this.name = 'ProfileStorageError';
        this.code = code;
        this.originalError = originalError;
    }
}

class ProfileValidationError extends Error {
    constructor(message, validationErrors = []) {
        super(message);
        this.name = 'ProfileValidationError';
        this.validationErrors = validationErrors;
    }
}

/**
 * Storage wrapper with error handling and validation
 */
class ProfileStorage {
    /**
     * Safely execute a storage operation with error handling
     * @param {Function} operation - Storage operation to execute
     * @param {Function} fallback - Fallback function if operation fails
     * @returns {*} Result of operation or fallback
     */
    static safeStorageOperation(operation, fallback = null) {
        try {
            return operation();
        } catch (error) {
            if (error.name === 'QuotaExceededError') {
                throw new ProfileStorageError(
                    'Profile storage quota exceeded. Please delete unused profiles.',
                    'QUOTA_EXCEEDED',
                    error
                );
            } else if (error.name === 'SecurityError') {
                console.warn('LocalStorage access denied, falling back to memory storage');
                return fallback ? fallback() : null;
            } else {
                throw new ProfileStorageError(
                    'Profile storage operation failed',
                    'STORAGE_ERROR',
                    error
                );
            }
        }
    }

    /**
     * Store data in LocalStorage
     * @param {string} key - Storage key
     * @param {*} data - Data to store
     */
    static setItem(key, data) {
        return this.safeStorageOperation(() => {
            const serialized = JSON.stringify(data);
            localStorage.setItem(key, serialized);
            return true;
        });
    }

    /**
     * Retrieve data from LocalStorage
     * @param {string} key - Storage key
     * @returns {*} Parsed data or null if not found
     */
    static getItem(key) {
        return this.safeStorageOperation(() => {
            const stored = localStorage.getItem(key);
            return stored ? JSON.parse(stored) : null;
        });
    }

    /**
     * Remove item from LocalStorage
     * @param {string} key - Storage key
     */
    static removeItem(key) {
        return this.safeStorageOperation(() => {
            localStorage.removeItem(key);
            return true;
        });
    }

    /**
     * Check if LocalStorage is available
     * @returns {boolean} True if LocalStorage is available
     */
    static isAvailable() {
        try {
            const test = 'tinkertools.storage.test';
            localStorage.setItem(test, 'test');
            localStorage.removeItem(test);
            return true;
        } catch (error) {
            return false;
        }
    }

    /**
     * Get current storage usage
     * @returns {Object} Storage usage information
     */
    static getUsage() {
        let totalSize = 0;
        let profileCount = 0;
        
        for (let key in localStorage) {
            if (key.startsWith(TINKER_PROFILES_CONFIG.storageKeys.profilePrefix)) {
                const value = localStorage.getItem(key);
                totalSize += key.length + (value ? value.length : 0);
                profileCount++;
            }
        }
        
        return {
            totalSize,
            profileCount,
            maxSize: TINKER_PROFILES_CONFIG.storage.maxProfiles * TINKER_PROFILES_CONFIG.storage.maxProfileSize,
            percentUsed: (totalSize / (TINKER_PROFILES_CONFIG.storage.maxProfiles * TINKER_PROFILES_CONFIG.storage.maxProfileSize)) * 100
        };
    }
}

/**
 * Profile validation and schema management
 */
class ProfileValidator {
    /**
     * Default profile schema for validation
     */
    static getDefaultSchema() {
        return {
            meta: {
                profileId: '',
                version: TINKER_PROFILES_CONFIG.version,
                created: new Date().toISOString(),
                modified: new Date().toISOString(),
                schemaVersion: TINKER_PROFILES_CONFIG.schemaVersion
            },
            character: {
                name: '',
                profession: '',
                level: 220,
                faction: 'Neutral',
                expansion: 'All',
                accountType: 'Paid'
            },
            attributes: {
                strength: 1000,
                stamina: 1000,
                agility: 1000,
                intelligence: 1000,
                sense: 1000,
                psychic: 1000
            },
            skills: {
                materialMetamorphosis: 2500,
                biologicalMetamorphosis: 2500,
                materialCreation: 2500,
                timeSpace: 2500,
                psychicModification: 2500,
                sensoryImprovement: 2500,
                weaponSkills: {
                    '1hBlunt': 1000,
                    '1hEdged': 1000,
                    '2hBlunt': 1000,
                    '2hEdged': 1000,
                    'pistol': 1000,
                    'rifle': 1000,
                    'shotgun': 1000,
                    'assaultRifle': 1000,
                    'submachineGun': 1000,
                    'bow': 1000,
                    'thrown': 1000,
                    'grenade': 1000
                }
            },
            appData: {
                tinkerItems: {
                    favorites: [],
                    recentSearches: [],
                    filters: {
                        showOnlyUsable: true,
                        levelRange: { min: 200, max: 220 }
                    }
                },
                tinkerPlants: {
                    implantConfig: {
                        head: { implant: null, shiny: null, bright: null, faded: null, ql: 300 },
                        eye: { implant: null, shiny: null, bright: null, faded: null, ql: 300 },
                        ear: { implant: null, shiny: null, bright: null, faded: null, ql: 300 },
                        rarm: { implant: null, shiny: null, bright: null, faded: null, ql: 300 },
                        chest: { implant: null, shiny: null, bright: null, faded: null, ql: 300 },
                        larm: { implant: null, shiny: null, bright: null, faded: null, ql: 300 },
                        waist: { implant: null, shiny: null, bright: null, faded: null, ql: 300 },
                        rwrist: { implant: null, shiny: null, bright: null, faded: null, ql: 300 },
                        leg: { implant: null, shiny: null, bright: null, faded: null, ql: 300 },
                        lwrist: { implant: null, shiny: null, bright: null, faded: null, ql: 300 },
                        rhand: { implant: null, shiny: null, bright: null, faded: null, ql: 300 },
                        lhand: { implant: null, shiny: null, bright: null, faded: null, ql: 300 },
                        feet: { implant: null, shiny: null, bright: null, faded: null, ql: 300 }
                    },
                    attributePreferences: {
                        strength: true,
                        stamina: true,
                        agility: false,
                        intelligence: true,
                        sense: false,
                        psychic: true
                    },
                    savedBuilds: []
                },
                tinkerNanos: {
                    filters: {
                        profession: [],
                        expansion: ['SL', 'AI'],
                        fpAble: true,
                        nanodeck: false
                    },
                    favorites: []
                },
                tinkerNukes: {
                    preferences: {
                        specialization: 1,
                        deckType: 1,
                        attackCapFocus: true,
                        dotPreference: false
                    },
                    savedSetups: []
                },
                tinkerFite: {
                    weaponPreferences: {
                        damageTypes: ['energy', 'projectile'],
                        weaponTypes: ['rifle', 'pistol'],
                        wrangleType: 131
                    },
                    savedBuilds: []
                },
                tinkerPocket: {
                    tracking: {
                        completedBosses: [],
                        wantedSymbiants: [],
                        ownedSymbiants: []
                    },
                    filters: {
                        levelRange: { min: 200, max: 220 },
                        slotPreferences: ['head', 'chest']
                    }
                }
            }
        };
    }

    /**
     * Validate a profile object against the schema
     * @param {Object} profileData - Profile data to validate
     * @throws {ProfileValidationError} If validation fails
     * @returns {boolean} True if valid
     */
    static validateProfile(profileData) {
        const errors = [];

        // Validate required fields
        if (!profileData.character || !profileData.character.name) {
            errors.push('Character name is required');
        }

        if (!profileData.character || !profileData.character.profession) {
            errors.push('Character profession is required');
        }

        // Validate character name
        if (profileData.character && profileData.character.name) {
            const name = profileData.character.name.trim();
            if (name.length < 1 || name.length > 32) {
                errors.push('Character name must be 1-32 characters');
            }
            if (!/^[a-zA-Z][a-zA-Z0-9]*$/.test(name)) {
                errors.push('Character name must start with letter and contain only alphanumeric characters');
            }
        }

        // Validate profession
        if (profileData.character && profileData.character.profession) {
            if (!TINKER_PROFILES_CONFIG.professions.includes(profileData.character.profession)) {
                errors.push(`Invalid profession: ${profileData.character.profession}`);
            }
        }

        // Validate level
        if (profileData.character && profileData.character.level !== undefined) {
            const level = parseInt(profileData.character.level);
            if (isNaN(level) || level < 1 || level > 220) {
                errors.push('Character level must be between 1 and 220');
            }
        }

        // Validate faction
        if (profileData.character && profileData.character.faction) {
            const validFactions = ['Omni', 'Clan', 'Neutral'];
            if (!validFactions.includes(profileData.character.faction)) {
                errors.push(`Invalid faction: ${profileData.character.faction}`);
            }
        }

        // Validate account type
        if (profileData.character && profileData.character.accountType) {
            const validAccountTypes = ['Froob', 'Paid'];
            if (!validAccountTypes.includes(profileData.character.accountType)) {
                errors.push(`Invalid account type: ${profileData.character.accountType}`);
            }
        }

        if (errors.length > 0) {
            throw new ProfileValidationError('Profile validation failed', errors);
        }

        return true;
    }

    /**
     * Sanitize user input to prevent XSS
     * @param {string} input - Input to sanitize
     * @returns {string} Sanitized input
     */
    static sanitizeInput(input) {
        if (typeof input !== 'string') return input;
        
        return input
            .replace(/[<>"']/g, '') // Remove potential HTML/JS injection
            .trim()
            .substring(0, 1000); // Limit length
    }

    /**
     * Normalize profile data to ensure consistency
     * @param {Object} profileData - Profile data to normalize
     * @returns {Object} Normalized profile data
     */
    static normalizeProfile(profileData) {
        const schema = this.getDefaultSchema();
        const normalized = JSON.parse(JSON.stringify(schema)); // Deep clone

        // Merge provided data with defaults
        if (profileData.character) {
            Object.assign(normalized.character, profileData.character);
            // Sanitize character name
            if (normalized.character.name) {
                normalized.character.name = this.sanitizeInput(normalized.character.name);
            }
        }

        if (profileData.attributes) {
            Object.assign(normalized.attributes, profileData.attributes);
        }

        if (profileData.skills) {
            Object.assign(normalized.skills, profileData.skills);
            if (profileData.skills.weaponSkills) {
                Object.assign(normalized.skills.weaponSkills, profileData.skills.weaponSkills);
            }
        }

        if (profileData.appData) {
            Object.keys(profileData.appData).forEach(appName => {
                if (normalized.appData[appName] && profileData.appData[appName]) {
                    normalized.appData[appName] = this.deepMerge(
                        normalized.appData[appName],
                        profileData.appData[appName]
                    );
                }
            });
        }

        return normalized;
    }

    /**
     * Deep merge two objects
     * @param {Object} target - Target object
     * @param {Object} source - Source object
     * @returns {Object} Merged object
     */
    static deepMerge(target, source) {
        const result = { ...target };
        
        for (const key in source) {
            if (source[key] && typeof source[key] === 'object' && !Array.isArray(source[key])) {
                result[key] = this.deepMerge(result[key] || {}, source[key]);
            } else {
                result[key] = source[key];
            }
        }
        
        return result;
    }
}

/**
 * Event system for profile changes
 */
class ProfileEventSystem {
    constructor() {
        this.listeners = new Map();
    }

    /**
     * Add event listener
     * @param {string} eventType - Event type to listen for
     * @param {Function} callback - Callback function
     */
    addEventListener(eventType, callback) {
        if (!this.listeners.has(eventType)) {
            this.listeners.set(eventType, new Set());
        }
        this.listeners.get(eventType).add(callback);
    }

    /**
     * Remove event listener
     * @param {string} eventType - Event type
     * @param {Function} callback - Callback function to remove
     */
    removeEventListener(eventType, callback) {
        if (this.listeners.has(eventType)) {
            this.listeners.get(eventType).delete(callback);
        }
    }

    /**
     * Dispatch event to all listeners
     * @param {string} eventType - Event type
     * @param {*} data - Event data
     */
    dispatchEvent(eventType, data) {
        if (this.listeners.has(eventType)) {
            const event = {
                type: eventType,
                detail: data,
                timestamp: Date.now()
            };

            this.listeners.get(eventType).forEach(callback => {
                try {
                    callback(event);
                } catch (error) {
                    console.error(`Error in event listener for ${eventType}:`, error);
                }
            });
        }

        // Also dispatch as custom DOM event for broader compatibility
        if (typeof window !== 'undefined' && window.dispatchEvent) {
            const customEvent = new CustomEvent(eventType, {
                detail: data
            });
            window.dispatchEvent(customEvent);
        }
    }
}

/**
 * Main TinkerProfiles class - Core Character Profile Management API
 */
class TinkerProfiles {
    constructor() {
        this.eventSystem = new ProfileEventSystem();
        this.cache = new Map();
        this.cacheTimestamps = new Map();
        this.initialized = false;
    }

    /**
     * Initialize the profile system
     * @returns {boolean} True if initialization successful
     */
    static init() {
        if (!TinkerProfiles.instance) {
            TinkerProfiles.instance = new TinkerProfiles();
        }

        if (!ProfileStorage.isAvailable()) {
            console.warn('LocalStorage not available, using memory storage');
            TinkerProfiles.instance.initialized = false;
            return false;
        }

        // Initialize metadata if not exists
        const meta = ProfileStorage.getItem(TINKER_PROFILES_CONFIG.storageKeys.profilesMeta);
        if (!meta) {
            ProfileStorage.setItem(TINKER_PROFILES_CONFIG.storageKeys.profilesMeta, {
                version: TINKER_PROFILES_CONFIG.version,
                created: new Date().toISOString(),
                profiles: []
            });
        }

        TinkerProfiles.instance.initialized = true;
        return true;
    }

    /**
     * Get the singleton instance
     * @returns {TinkerProfiles} Instance
     */
    static getInstance() {
        if (!TinkerProfiles.instance) {
            TinkerProfiles.init();
        }
        return TinkerProfiles.instance;
    }

    /**
     * Generate a UUID v4 for profile IDs
     * @returns {string} UUID v4 string
     */
    static generateProfileId() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            const r = Math.random() * 16 | 0;
            const v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }

    /**
     * Create a new character profile
     * @param {Object} characterData - Character data for the profile
     * @returns {string} Profile ID of created profile
     */
    static createProfile(characterData) {
        if (!TinkerProfiles.getInstance().initialized) {
            throw new ProfileStorageError('Profile system not initialized', 'NOT_INITIALIZED');
        }

        // Validate input data
        ProfileValidator.validateProfile(characterData);

        // Generate profile ID and normalize data
        const profileId = this.generateProfileId();
        const profileData = ProfileValidator.normalizeProfile(characterData);
        
        // Set metadata
        profileData.meta = {
            profileId: profileId,
            version: TINKER_PROFILES_CONFIG.version,
            created: new Date().toISOString(),
            modified: new Date().toISOString(),
            schemaVersion: TINKER_PROFILES_CONFIG.schemaVersion
        };

        // Check storage limits
        const usage = ProfileStorage.getUsage();
        if (usage.profileCount >= TINKER_PROFILES_CONFIG.storage.maxProfiles) {
            throw new ProfileStorageError(
                `Maximum number of profiles (${TINKER_PROFILES_CONFIG.storage.maxProfiles}) reached`,
                'MAX_PROFILES_EXCEEDED'
            );
        }

        // Store the profile
        const profileKey = TINKER_PROFILES_CONFIG.storageKeys.profilePrefix + profileId;
        ProfileStorage.setItem(profileKey, profileData);

        // Update metadata
        const meta = ProfileStorage.getItem(TINKER_PROFILES_CONFIG.storageKeys.profilesMeta);
        meta.profiles.push({
            profileId: profileId,
            name: profileData.character.name,
            profession: profileData.character.profession,
            level: profileData.character.level,
            created: profileData.meta.created,
            modified: profileData.meta.modified
        });
        ProfileStorage.setItem(TINKER_PROFILES_CONFIG.storageKeys.profilesMeta, meta);

        // Clear cache
        TinkerProfiles.getInstance().cache.delete(profileId);

        // Dispatch event
        TinkerProfiles.getInstance().eventSystem.dispatchEvent(PROFILE_EVENTS.PROFILE_CREATED, {
            profileId: profileId,
            profile: profileData
        });

        return profileId;
    }

    /**
     * Get a profile by ID
     * @param {string} profileId - Profile ID
     * @returns {Object|null} Profile data or null if not found
     */
    static getProfile(profileId) {
        if (!profileId) return null;

        const instance = TinkerProfiles.getInstance();
        
        // Check cache first
        const cached = instance.cache.get(profileId);
        const timestamp = instance.cacheTimestamps.get(profileId);
        
        if (cached && timestamp && (Date.now() - timestamp) < TINKER_PROFILES_CONFIG.storage.cacheTimeout) {
            return cached;
        }

        // Load from storage
        const profileKey = TINKER_PROFILES_CONFIG.storageKeys.profilePrefix + profileId;
        const profile = ProfileStorage.getItem(profileKey);
        
        if (profile) {
            // Cache the profile
            instance.cache.set(profileId, profile);
            instance.cacheTimestamps.set(profileId, Date.now());
        }

        return profile;
    }

    /**
     * Update a profile
     * @param {string} profileId - Profile ID
     * @param {Object} updates - Updates to apply
     * @returns {boolean} True if update successful
     */
    static updateProfile(profileId, updates) {
        const profile = this.getProfile(profileId);
        if (!profile) {
            throw new Error(`Profile ${profileId} not found`);
        }

        // Deep merge updates
        const updatedProfile = ProfileValidator.deepMerge(profile, updates);
        updatedProfile.meta.modified = new Date().toISOString();

        // Validate updated profile
        ProfileValidator.validateProfile(updatedProfile);

        // Store updated profile
        const profileKey = TINKER_PROFILES_CONFIG.storageKeys.profilePrefix + profileId;
        ProfileStorage.setItem(profileKey, updatedProfile);

        // Update metadata
        const meta = ProfileStorage.getItem(TINKER_PROFILES_CONFIG.storageKeys.profilesMeta);
        const profileIndex = meta.profiles.findIndex(p => p.profileId === profileId);
        if (profileIndex !== -1) {
            meta.profiles[profileIndex].name = updatedProfile.character.name;
            meta.profiles[profileIndex].profession = updatedProfile.character.profession;
            meta.profiles[profileIndex].level = updatedProfile.character.level;
            meta.profiles[profileIndex].modified = updatedProfile.meta.modified;
            ProfileStorage.setItem(TINKER_PROFILES_CONFIG.storageKeys.profilesMeta, meta);
        }

        // Clear cache
        const instance = TinkerProfiles.getInstance();
        instance.cache.delete(profileId);

        // Dispatch event
        instance.eventSystem.dispatchEvent(PROFILE_EVENTS.PROFILE_UPDATED, {
            profileId: profileId,
            profile: updatedProfile,
            updates: updates
        });

        return true;
    }

    /**
     * Delete a profile
     * @param {string} profileId - Profile ID to delete
     * @returns {boolean} True if deletion successful
     */
    static deleteProfile(profileId) {
        const profile = this.getProfile(profileId);
        if (!profile) {
            return false;
        }

        // Remove from storage
        const profileKey = TINKER_PROFILES_CONFIG.storageKeys.profilePrefix + profileId;
        ProfileStorage.removeItem(profileKey);

        // Update metadata
        const meta = ProfileStorage.getItem(TINKER_PROFILES_CONFIG.storageKeys.profilesMeta);
        meta.profiles = meta.profiles.filter(p => p.profileId !== profileId);
        ProfileStorage.setItem(TINKER_PROFILES_CONFIG.storageKeys.profilesMeta, meta);

        // Clear from cache
        const instance = TinkerProfiles.getInstance();
        instance.cache.delete(profileId);
        instance.cacheTimestamps.delete(profileId);

        // Clear active profile if it was the deleted one
        const activeProfileId = this.getActiveProfileId();
        if (activeProfileId === profileId) {
            ProfileStorage.removeItem(TINKER_PROFILES_CONFIG.storageKeys.activeProfile);
        }

        // Dispatch event
        instance.eventSystem.dispatchEvent(PROFILE_EVENTS.PROFILE_DELETED, {
            profileId: profileId,
            profile: profile
        });

        return true;
    }

    /**
     * Get list of all profiles (metadata only)
     * @returns {Array} Array of profile metadata
     */
    static getProfileList() {
        const meta = ProfileStorage.getItem(TINKER_PROFILES_CONFIG.storageKeys.profilesMeta);
        return meta ? meta.profiles : [];
    }

    /**
     * Set the active profile
     * @param {string} profileId - Profile ID to set as active
     * @returns {boolean} True if successful
     */
    static setActiveProfile(profileId) {
        const profile = this.getProfile(profileId);
        if (!profile) {
            throw new Error(`Profile ${profileId} not found`);
        }

        const oldProfileId = this.getActiveProfileId();
        ProfileStorage.setItem(TINKER_PROFILES_CONFIG.storageKeys.activeProfile, profileId);

        // Dispatch event
        TinkerProfiles.getInstance().eventSystem.dispatchEvent(PROFILE_EVENTS.ACTIVE_CHANGED, {
            newProfileId: profileId,
            oldProfileId: oldProfileId,
            profile: profile
        });

        return true;
    }

    /**
     * Get the active profile
     * @returns {Object|null} Active profile data or null
     */
    static getActiveProfile() {
        const activeProfileId = this.getActiveProfileId();
        return activeProfileId ? this.getProfile(activeProfileId) : null;
    }

    /**
     * Get the active profile ID
     * @returns {string|null} Active profile ID or null
     */
    static getActiveProfileId() {
        return ProfileStorage.getItem(TINKER_PROFILES_CONFIG.storageKeys.activeProfile);
    }

    /**
     * Get app-specific data from a profile
     * @param {string} profileId - Profile ID
     * @param {string} appName - Application name
     * @returns {Object|null} App data or null
     */
    static getAppData(profileId, appName) {
        const profile = this.getProfile(profileId);
        return profile && profile.appData && profile.appData[appName] ? profile.appData[appName] : null;
    }

    /**
     * Update app-specific data in a profile
     * @param {string} profileId - Profile ID
     * @param {string} appName - Application name
     * @param {Object} data - Data to set
     * @returns {boolean} True if successful
     */
    static updateAppData(profileId, appName, data) {
        return this.updateProfile(profileId, {
            appData: {
                [appName]: data
            }
        });
    }

    /**
     * Merge app-specific data in a profile
     * @param {string} profileId - Profile ID
     * @param {string} appName - Application name
     * @param {Object} updates - Updates to merge
     * @returns {boolean} True if successful
     */
    static mergeAppData(profileId, appName, updates) {
        const profile = this.getProfile(profileId);
        if (!profile) {
            throw new Error(`Profile ${profileId} not found`);
        }

        const currentAppData = profile.appData[appName] || {};
        const mergedAppData = ProfileValidator.deepMerge(currentAppData, updates);

        return this.updateAppData(profileId, appName, mergedAppData);
    }

    /**
     * Export a profile to JSON
     * @param {string} profileId - Profile ID to export
     * @returns {string} JSON string of profile data
     */
    static exportProfile(profileId) {
        const profile = this.getProfile(profileId);
        if (!profile) {
            throw new Error(`Profile ${profileId} not found`);
        }

        return JSON.stringify(profile, null, 2);
    }

    /**
     * Export all profiles to JSON
     * @returns {string} JSON string of all profiles
     */
    static exportAllProfiles() {
        const profileList = this.getProfileList();
        const profiles = profileList.map(meta => this.getProfile(meta.profileId)).filter(p => p !== null);
        
        return JSON.stringify({
            version: TINKER_PROFILES_CONFIG.version,
            exported: new Date().toISOString(),
            profiles: profiles
        }, null, 2);
    }

    /**
     * Import a profile from JSON data
     * @param {string} profileData - JSON string of profile data
     * @returns {string} Profile ID of imported profile
     */
    static importProfile(profileData) {
        let parsedData;
        try {
            parsedData = typeof profileData === 'string' ? JSON.parse(profileData) : profileData;
        } catch (error) {
            throw new Error('Invalid JSON data for profile import');
        }

        // Validate imported data
        ProfileValidator.validateProfile(parsedData);

        // Generate new profile ID to avoid conflicts
        const newProfileId = this.generateProfileId();
        const normalizedData = ProfileValidator.normalizeProfile(parsedData);
        
        // Update character name if duplicate exists
        const existingProfiles = this.getProfileList();
        let characterName = normalizedData.character.name;
        let counter = 1;
        
        while (existingProfiles.some(p => p.name === characterName)) {
            characterName = `${normalizedData.character.name} (${counter})`;
            counter++;
        }
        
        normalizedData.character.name = characterName;

        // Create the profile
        return this.createProfile(normalizedData);
    }

    /**
     * Import multiple profiles from JSON data
     * @param {string} profilesData - JSON string containing multiple profiles
     * @returns {Array} Array of imported profile IDs
     */
    static importProfiles(profilesData) {
        let parsedData;
        try {
            parsedData = typeof profilesData === 'string' ? JSON.parse(profilesData) : profilesData;
        } catch (error) {
            throw new Error('Invalid JSON data for profiles import');
        }

        if (!parsedData.profiles || !Array.isArray(parsedData.profiles)) {
            throw new Error('Invalid profiles data format');
        }

        const importedIds = [];
        for (const profileData of parsedData.profiles) {
            try {
                const profileId = this.importProfile(profileData);
                importedIds.push(profileId);
            } catch (error) {
                console.error('Failed to import profile:', error);
                // Continue with other profiles
            }
        }

        return importedIds;
    }

    /**
     * Validate profile data
     * @param {Object} profileData - Profile data to validate
     * @returns {boolean} True if valid
     */
    static validateProfile(profileData) {
        return ProfileValidator.validateProfile(profileData);
    }

    /**
     * Get current schema version
     * @returns {string} Current schema version
     */
    static getCurrentSchemaVersion() {
        return TINKER_PROFILES_CONFIG.schemaVersion;
    }

    /**
     * Migrate profile to target version (placeholder for future use)
     * @param {Object} profileData - Profile data to migrate
     * @param {string} targetVersion - Target schema version
     * @returns {Object} Migrated profile data
     */
    static migrateProfile(profileData, targetVersion) {
        // For now, just return the data as-is
        // In the future, this will handle schema migrations
        return profileData;
    }

    /**
     * Add event listener
     * @param {string} eventType - Event type
     * @param {Function} callback - Callback function
     */
    static addEventListener(eventType, callback) {
        TinkerProfiles.getInstance().eventSystem.addEventListener(eventType, callback);
    }

    /**
     * Remove event listener
     * @param {string} eventType - Event type
     * @param {Function} callback - Callback function
     */
    static removeEventListener(eventType, callback) {
        TinkerProfiles.getInstance().eventSystem.removeEventListener(eventType, callback);
    }

    /**
     * Dispatch event
     * @param {string} eventType - Event type
     * @param {*} data - Event data
     */
    static dispatchEvent(eventType, data) {
        TinkerProfiles.getInstance().eventSystem.dispatchEvent(eventType, data);
    }

    /**
     * Get storage usage information
     * @returns {Object} Storage usage data
     */
    static getStorageUsage() {
        return ProfileStorage.getUsage();
    }

    /**
     * Clean up storage by removing orphaned data
     * @returns {Object} Cleanup results
     */
    static cleanupStorage() {
        const meta = ProfileStorage.getItem(TINKER_PROFILES_CONFIG.storageKeys.profilesMeta);
        if (!meta) return { removedProfiles: 0, errors: [] };

        const validProfileIds = new Set(meta.profiles.map(p => p.profileId));
        const removedProfiles = [];
        const errors = [];

        // Check all profile keys in storage
        for (let key in localStorage) {
            if (key.startsWith(TINKER_PROFILES_CONFIG.storageKeys.profilePrefix)) {
                const profileId = key.substring(TINKER_PROFILES_CONFIG.storageKeys.profilePrefix.length);
                
                if (!validProfileIds.has(profileId)) {
                    try {
                        ProfileStorage.removeItem(key);
                        removedProfiles.push(profileId);
                    } catch (error) {
                        errors.push(`Failed to remove ${key}: ${error.message}`);
                    }
                }
            }
        }

        // Clear cache
        const instance = TinkerProfiles.getInstance();
        instance.cache.clear();
        instance.cacheTimestamps.clear();

        return {
            removedProfiles: removedProfiles.length,
            profileIds: removedProfiles,
            errors: errors
        };
    }
}

// Static instance property
TinkerProfiles.instance = null;

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        TinkerProfiles,
        PROFILE_EVENTS,
        ProfileStorageError,
        ProfileValidationError
    };
}

// Auto-initialize when DOM is ready
if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            TinkerProfiles.init();
        });
    } else {
        TinkerProfiles.init();
    }
}