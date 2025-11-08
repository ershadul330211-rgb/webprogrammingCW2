<template>
  <div class="container my-4">
    <header class="d-flex justify-content-between align-items-center mb-3 p-3 bg-light rounded shadow-sm">
      <h1><i class="bi bi-people-fill"></i> Gintama Characters</h1>
      <button class="btn btn-primary btn-lg" @click="openCharacterModal(null)">
        <i class="bi bi-plus-circle-fill me-2"></i>Add New Character
      </button>
    </header>

    <CharacterAccordion
      :key="characterListKey" 
      :characters="characters"
      @edit-character="openCharacterModal"
      @delete-character="handleDeleteCharacter"
      @add-quote="openQuoteModal"
      @edit-quote="openQuoteModal"
      @delete-quote="handleDeleteQuote"
    />

    <CharacterModal
      :show="showCharacterModal"
      :character="selectedCharacter"
      @close="showCharacterModal = false"
      @save="handleSaveCharacter"
    />

    <QuoteModal
      :show="showQuoteModal"
      :quote="selectedQuote"
      :characterId="selectedCharacterId"
      @close="showQuoteModal = false"
      @save="handleSaveQuote"
    />
  </div>
</template>

<script>
// Import child components
import CharacterAccordion from './components/CharacterAccordion.vue';
import CharacterModal from './components/CharacterModal.vue';
import QuoteModal from './components/QuoteModal.vue';

// Define the base URL for the API
const API_URL = 'http://127.0.0.1:8000/api';

export default {
  name: 'App',
  components: {
    CharacterAccordion,
    CharacterModal,
    QuoteModal,
  },
  // Options API
  data() {
    return {
      characters: [],
      showCharacterModal: false,
      showQuoteModal: false,
      selectedCharacter: null, // For editing a character
      selectedQuote: null, // For editing a quote
      selectedCharacterId: null, // For creating a new quote
      characterListKey: 0, // <-- THIS IS THE FIX (Part 2)
    };
  },
  methods: {
    /**
     * Forces the <CharacterAccordion> component to re-render itself.
     * This is the fix for the Bootstrap/Vue reactivity bug.
     */
    forceRerender() {
      this.characterListKey += 1;
    },

    /**
     * Helper function to find and replace a character in the local data.
     */
    updateCharacterInList(updatedCharacter) {
        const index = this.characters.findIndex(c => c.id === updatedCharacter.id);
        if (index !== -1) {
            this.characters.splice(index, 1, updatedCharacter);
        }
    },

    // --- Data Fetching (GET) ---
    async fetchCharacters() {
      try {
        const response = await fetch(`${API_URL}/characters/`);
        this.characters = await response.json();
      } catch (error) {
        console.error('Error fetching characters:', error);
      }
    },

    // --- Modal Triggers ---
    openCharacterModal(character) {
      this.selectedCharacter = character ? { ...character } : null; // Use copy
      this.showCharacterModal = true;
    },
    
    openQuoteModal(item) {
      if (item.hasOwnProperty('quotes')) { // It's a Character (for adding)
        this.selectedQuote = null;
        this.selectedCharacterId = item.id;
      } else { // It's a Quote (for editing)
        this.selectedQuote = { ...item }; // Use copy
        this.selectedCharacterId = item.character_id;
      }
      this.showQuoteModal = true;
    },

    // --- API Call: Save/Update Character (POST / PUT) ---
    async handleSaveCharacter(characterData) {
      const isUpdating = !!characterData.id;
      const url = isUpdating
        ? `${API_URL}/characters/${characterData.id}/`
        : `${API_URL}/characters/`;
      const method = isUpdating ? 'PUT' : 'POST';

      try {
        const response = await fetch(url, {
          method: method,
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(characterData),
        });
        
        this.showCharacterModal = false; // Close modal
        
        // Wait for modal to close, then update data & force re-render
        setTimeout(async () => {
          await this.fetchCharacters(); // Re-fetch all
          this.forceRerender(); // Force UI update
        }, 300); // 300ms is a safe delay for the animation

      } catch (error) {
        console.error('Error saving character:', error);
      }
    },

    // --- API Call: Delete Character (DELETE) ---
    async handleDeleteCharacter(characterId) {
      if (!confirm('Are you sure you want to delete this character?')) return;

      try {
        await fetch(`${API_URL}/characters/${characterId}/`, { method: 'DELETE' });
        // Update list locally and force re-render
        this.characters = this.characters.filter(c => c.id !== characterId);
        this.forceRerender();
      } catch (error) {
        console.error('Error deleting character:', error);
      }
    },

    // --- API Call: Save/Update Quote (POST / PUT) ---
    async handleSaveQuote(quoteData) {
      const isUpdating = !!quoteData.id;
      const url = isUpdating 
        ? `${API_URL}/quotes/${quoteData.id}/` 
        : `${API_URL}/quotes/`;
      const method = isUpdating ? 'PUT' : 'POST';

      if (!isUpdating) {
        quoteData.character_id = this.selectedCharacterId;
      }
      
      try {
        const response = await fetch(url, {
          method: method,
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(quoteData),
        });
        
        const updatedCharacter = await response.json();
        this.showQuoteModal = false; // Close modal

        // Wait for modal to close, then update data & force re-render
        setTimeout(() => {
          this.updateCharacterInList(updatedCharacter); 
          this.forceRerender();
        }, 300);

      } catch (error) {
        console.error('Error saving quote:', error);
      }
    },

    // --- API Call: Delete Quote (DELETE) ---
    async handleDeleteQuote(quoteId) {
      if (!confirm('Are you sure you want to delete this quote?')) return;

      try {
        const response = await fetch(`${API_URL}/quotes/${quoteId}/`, {
          method: 'DELETE',
        });
        
        const updatedCharacter = await response.json();
        this.updateCharacterInList(updatedCharacter);
        this.forceRerender();
      } catch (error) {
        console.error('Error deleting quote:', error);
      }
    },
  },
  mounted() {
    // Fetch initial data when the component loads
    this.fetchCharacters();
  },
};
</script>

<style>
/* Import Bootstrap Icons */
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css");

/* Small style tweak for quotes */
.blockquote {
  font-size: 1rem;
}
</style>