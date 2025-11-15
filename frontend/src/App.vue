<template>
  <div class="container my-4">
    <header class="d-flex justify-content-between align-items-center mb-3 p-3 bg-light rounded shadow-sm">
      <h1><i class="bi bi-people-fill"></i> Gintama Characters</h1>
      <button class="btn btn-primary btn-lg" @click="openCharacterModal(null)">
        <i class="bi bi-plus-circle-fill me-2"></i>Add New Character
      </button>
    </header>

    <CharacterAccordion
      :key="accordionKey" 
      :characters="characters"
      @edit-character="openCharacterModal"
      @delete-character="DeleteCharacter"
      @add-quote="openQuoteModal"
      @edit-quote="openQuoteModal"
      @delete-quote="DeleteQuote"
    />

    <CharacterModal
      :show="showCharacterModal"
      :character="selectedCharacter"
      @close="showCharacterModal = false"
      @save="SaveCharacter"
    />

    <QuoteModal
      :show="showQuoteModal"
      :quote="selectedQuote"
      :characterId="selectedCharacterId"
      @close="showQuoteModal = false"
      @save="SaveQuote"
    />
  </div>
</template>

<script>
import CharacterAccordion from './components/CharacterAccordion.vue';
import CharacterModal from './components/CharacterModal.vue';
import QuoteModal from './components/QuoteModal.vue';

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
      selectedCharacterId: null, // For adding a quote
      accordionKey: 0, 
    };
  },
  methods: {
    // Force the accordian to update by changing its key
    refreshAccordion() {
      this.accordionKey += 1;
    },

    // Finds and updates a character in the local list
    updateList(updatedCharacter) {
        const index = this.characters.findIndex(c => c.id === updatedCharacter.id);
        if (index !== -1) {
            this.characters.splice(index, 1, updatedCharacter);
        }
    },

    async fetchCharacters() {
      try {
        const response = await fetch(`${API_URL}/characters/`);
        this.characters = await response.json();
      } catch (error) {
        console.error('Error fetching characters:', error);
      }
    },

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

    async SaveCharacter(characterData) {
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
        
        setTimeout(async () => {
          await this.fetchCharacters();
          this.refreshAccordion(); 
        }, 300);

      } catch (error) {
        console.error('Error saving character:', error);
      }
    },

    async DeleteCharacter(characterId) {
      if (!confirm('Are you sure you want to delete this character?')) return;

      try {
        await fetch(`${API_URL}/characters/${characterId}/`, { method: 'DELETE' });
        // Update list locally and force re-render
        this.characters = this.characters.filter(c => c.id !== characterId);
        this.refreshAccordion();
      } catch (error) {
        console.error('Error deleting character:', error);
      }
    },

    async SaveQuote(quoteData) {
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
          this.updateList(updatedCharacter); 
          this.refreshAccordion();
        }, 300);

      } catch (error) {
        console.error('Error saving quote:', error);
      }
    },

    async DeleteQuote(quoteId) {
      if (!confirm('Are you sure you want to delete this quote?')) return;

      try {
        const response = await fetch(`${API_URL}/quotes/${quoteId}/`, {
          method: 'DELETE',
        });
        
        const updatedCharacter = await response.json();
        this.updateList(updatedCharacter);
        this.refreshAccordion();
      } catch (error) {
        console.error('Error deleting quote:', error);
      }
    },
  },
  mounted() {
    this.fetchCharacters();
  },
};
</script>

<style>
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css");

.blockquote {
  font-size: 1rem;
}
</style>