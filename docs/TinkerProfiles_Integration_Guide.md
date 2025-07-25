# TinkerProfiles Integration Guide

## Overview

The TinkerProfiles system has been successfully integrated into the shared base template (`templates/shared/base.html`). This provides a unified character profile management system across all TinkerTools applications.

## What's Included

### 1. Core JavaScript Libraries
- **`static/js/tinker-profiles.js`** - Core profile management API
- **`static/js/tinker-profiles-ui.js`** - UI components and interactions

### 2. Base Template Integration
- Profile selector dropdown in the navbar (positioned before the RK clock)
- Profile creation/edit modal
- Profile management modal with import/export functionality
- Notification system for user feedback
- Custom CSS styling for seamless Bootstrap integration

### 3. Global Utilities
- `window.TinkerToolsUtils` - Helper functions for applications
- Event system for profile changes
- Automatic initialization and setup

## Features

### Profile Selector
- Dropdown in the navbar showing current active profile
- Quick switching between profiles
- "Create New Profile" and "Manage Profiles" options
- Shows character name, level, and profession abbreviation

### Profile Creation/Editing
- Modal form for creating new profiles or editing existing ones
- Character information: Name, Profession, Level, Faction, Account Type, Expansion
- Optional attributes section (Strength, Stamina, Agility, Intelligence, Sense, Psychic)
- Form validation with Bootstrap styling
- Real-time feedback and error handling

### Profile Management
- Table view of all profiles with sortable columns
- Action buttons: Edit, Duplicate, Export, Delete
- Import/Export functionality for backup and sharing
- Storage usage display
- Bulk operations support

### Notifications
- Toast notifications for user feedback
- Success, error, warning, and info message types
- Auto-dismissing with configurable duration
- Positioned in top-right corner

## Usage for Application Developers

### Accessing Profile Data

```javascript
// Get the currently active profile
const profile = window.TinkerToolsUtils.getActiveProfile();

// Get app-specific data for your application
const myAppData = window.TinkerToolsUtils.getAppData('myAppName');

// Update app-specific data
window.TinkerToolsUtils.updateAppData('myAppName', {
    setting1: 'value1',
    setting2: 'value2'
});

// Merge updates into existing app data
window.TinkerToolsUtils.mergeAppData('myAppName', {
    newSetting: 'newValue'
});
```

### Listening for Profile Changes

```javascript
document.addEventListener('profileChanged', function(event) {
    const profile = event.detail.profile;
    const characterData = event.detail.characterData;
    const attributes = event.detail.attributes;
    const appData = event.detail.appData;
    
    // React to profile change
    console.log('Switched to:', characterData.name, characterData.profession);
    
    // Update your application UI/data
    updateApplicationForProfile(profile);
});
```

### Direct API Access

```javascript
// Direct access to TinkerProfiles API
if (window.TinkerProfiles) {
    // Create a new profile
    const profileId = TinkerProfiles.createProfile({
        character: {
            name: 'MyCharacter',
            profession: 'Agent',
            level: 220
        }
    });
    
    // Get a specific profile
    const profile = TinkerProfiles.getProfile(profileId);
    
    // Update profile data
    TinkerProfiles.updateProfile(profileId, {
        character: { level: 200 }
    });
    
    // Set active profile
    TinkerProfiles.setActiveProfile(profileId);
}
```

## App Data Structure

Each profile contains an `appData` object with sections for each TinkerTools application:

```javascript
{
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
            // ... other slots
        },
        attributePreferences: {
            strength: true,
            stamina: true,
            // ... other attributes
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
```

## Storage and Privacy

- **Client-side only**: All data stored in browser's LocalStorage
- **No server communication**: Complete user privacy
- **Storage limits**: 50 profiles max, 50KB per profile
- **Automatic cleanup**: Orphaned data detection and removal
- **Export/Import**: Full backup and restore capabilities

## Customization

### Styling
The integration includes custom CSS that follows Bootstrap patterns. You can override styles by targeting these classes:

```css
.profile-selector { /* Profile dropdown button */ }
.profile-selector .dropdown-menu { /* Dropdown menu */ }
.profile-selector .dropdown-item { /* Individual profile items */ }
#profile-modal { /* Profile creation/edit modal */ }
#profile-management-modal { /* Profile management modal */ }
#tinker-notifications { /* Notification container */ }
```

### Event Handling
You can listen for profile system events:

```javascript
// Profile events
TinkerProfiles.addEventListener('profile:created', (event) => {
    console.log('Profile created:', event.detail.profileId);
});

TinkerProfiles.addEventListener('profile:updated', (event) => {
    console.log('Profile updated:', event.detail.profileId);
});

TinkerProfiles.addEventListener('profile:deleted', (event) => {
    console.log('Profile deleted:', event.detail.profileId);
});

TinkerProfiles.addEventListener('profile:active:changed', (event) => {
    console.log('Active profile changed:', event.detail.newProfileId);
});
```

## Testing

A test file `test_integration.html` has been created to verify the integration. Open this file in a browser to:

1. Test profile system initialization
2. Create test profiles
3. Verify UI integration
4. Test event handling
5. Check localStorage functionality

## Backward Compatibility

The integration is designed to be completely backward compatible:

- **No breaking changes**: Existing functionality continues to work
- **Progressive enhancement**: Features activate when profiles are available
- **Graceful degradation**: Applications work without profiles
- **Optional usage**: Applications can choose their level of integration

## Troubleshooting

### Common Issues

1. **Profile selector not appearing**
   - Check browser console for JavaScript errors
   - Verify TinkerProfiles scripts are loading correctly
   - Ensure Bootstrap is properly included

2. **LocalStorage errors**
   - Check if browser allows LocalStorage (some privacy modes block it)
   - Verify storage quota hasn't been exceeded
   - Check for conflicting scripts

3. **Modal not working**
   - Ensure Bootstrap JavaScript is included
   - Check for Bootstrap version compatibility
   - Verify modal markup is complete

### Debug Information

```javascript
// Check if TinkerProfiles is loaded
console.log('TinkerProfiles available:', typeof TinkerProfiles !== 'undefined');

// Check storage usage
if (window.TinkerProfiles) {
    console.log('Storage usage:', TinkerProfiles.getStorageUsage());
}

// Check profile list
if (window.TinkerProfiles) {
    console.log('Profiles:', TinkerProfiles.getProfileList());
}
```

## Migration from Individual Tools

If you have existing TinkerTools applications that manage their own character data:

1. **Create migration function** to convert existing data to profile format
2. **Update data access patterns** to use the TinkerProfiles API
3. **Add profile change listeners** to update UI when profile switches
4. **Test thoroughly** to ensure data integrity

## Next Steps

1. **Test the integration** using the provided test file
2. **Update individual applications** to use the profile system
3. **Add profile-specific features** to enhance user experience
4. **Gather user feedback** and iterate on the implementation

## Support

For issues or questions about the TinkerProfiles integration:

1. Check the browser console for error messages
2. Verify all dependencies are properly loaded
3. Test with the integration test file
4. Review this documentation for usage patterns