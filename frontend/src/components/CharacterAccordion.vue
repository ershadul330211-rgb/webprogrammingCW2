<template>
  <div class="accordion"> <div v-if="!characters.length" class="alert alert-info text-center">
      No characters found. Add one to get started!
    </div>
    
    <div class="accordion-item" v-for="character in characters" :key="character.id">
      <h2 class="accordion-header" :id="'heading' + character.id">
        <button
          class="accordion-button collapsed"
          type="button"
          data-bs-toggle="collapse"
          :data-bs-target="'#collapse' + character.id"
        >
          <span class="h5 mb-0 me-auto">{{ character.name }}</span>
          <span v-if="character.is_samurai" class="badge bg-danger me-3">Samurai</span>
          <span v-if="character.age" class="badge bg-secondary me-3">Age: {{ character.age }}</span>
          <span v-if="character.birthday" class="badge bg-info me-3">Born: {{ character.birthday }}</span>
        </button>
      </h2>
      <div
        :id="'collapse' + character.id"
        class="accordion-collapse collapse"
        :aria-labelledby="'heading' + character.id"
        
        >
        <div class="accordion-body">
          <div class="d-flex justify-content-between align-items-start">
            <div>
              <h5>Bio</h5>
              <p style="white-space: pre-wrap;">{{ character.description }}</p>
            </div>
            
            <div>
              <button class="btn btn-sm btn-outline-secondary me-2" @click="$emit('edit-character', character)">
                <i class="bi bi-pencil-fill me-1"></i>Edit Character
              </button>
              <button class="btn btn-sm btn-outline-danger" @click="$emit('delete-character', character.id)">
                <i class="bi bi-trash-fill me-1"></i>Delete Character
              </button>
            </div>
          </div>
          
          <hr />
          
          <div class="d-flex justify-content-between align-items-center mb-2">
            <h5><i class="bi bi-chat-right-quote-fill"></i> Famous Quotes</h5>
            <button class="btn btn-sm btn-success" @click="$emit('add-quote', character)">
              <i class="bi bi-plus-lg me-1"></i>Add Quote
            </button>
          </div>
          
          <div v-if="!character.quotes.length">
             <p class="text-center text-muted">No quotes for this character.</p>
          </div>
          <div v-else>
            <figure v-for="quote in character.quotes" :key="quote.id" class="border-start border-4 border-secondary ps-3 mb-3">
              <blockquote class="blockquote">
                <p>{{ quote.text }}</p>
              </blockquote>
              <figcaption class="blockquote-footer d-flex justify-content-end">
                <div>
                  <button class="btn btn-sm btn-link text-secondary py-0" @click="$emit('edit-quote', quote)">
                    Edit
                  </button>
                  <button class="btn btn-sm btn-link text-danger py-0" @click="$emit('delete-quote', quote.id)">
                    Delete
                  </button>
                </div>
              </figcaption>
            </figure>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CharacterAccordion',
  props: {
    characters: {
      type: Array,
      required: true,
    },
  },
  // Declare all events this component can 'emit' up to the parent
  emits: [
    'edit-character',
    'delete-character',
    'add-quote',
    'edit-quote',
    'delete-quote',
  ],
};
</script>