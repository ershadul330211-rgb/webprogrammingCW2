<template>
  <div class="modal fade" ref="characterModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ formTitle }}</h5>
          <button type="button" class="btn-close" @click="closeModal"></button>
        </div>
        <form @submit.prevent="submitForm">
          <div class="modal-body">
            <div class="mb-3">
              <label for="charName" class="form-label">Name</label>
              <input type="text" class="form-control" id="charName" v-model="formData.name" required />
            </div>
            <div class="mb-3">
              <label for="charDesc" class="form-label">Description</label>
              <textarea class="form-control" id="charDesc" rows="4" v-model="formData.description" required></textarea>
            </div>
            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="charAge" class="form-label">Age</label>
                <input type="number" class="form-control" id="charAge" v-model.number="formData.age" min="0" />
              </div>
              <div class="col-md-6 mb-3">
                <label for="charBirthday" class="form-label">Birthday</label>
                <input type="date" class="form-control" id="charBirthday" v-model="formData.birthday" />
              </div>
            </div>
            <div class="form-check mb-3">
              <input class="form-check-input" type="checkbox" id="isSamurai" v-model="formData.is_samurai" />
              <label class="form-check-label" for="isSamurai">
                Is a Samurai?
              </label>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal">
              Close
            </button>
            <button type="submit" class="btn btn-primary">
              Save Character
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>

import { Modal } from 'bootstrap'; 

export default {
  name: 'CharacterModal',
  props: {
    show: Boolean, 
    character: Object, 
  },
  emits: ['close', 'save'], 
  data() {
    return {
      modalInstance: null,
      formData: {},
    };
  },
  computed: {
    formTitle() {
      return this.character ? 'Edit Character' : 'Add New Character';
    },
  },
  methods: {
    closeModal() {
      this.$emit('close'); 
    },
    submitForm() {
      this.$emit('save', this.formData);
    },
    resetForm() {
      this.formData = {
        name: '',
        description: '',
        age: null,
        birthday: null,
        is_samurai: false,
      };
    },
  },
  watch: {
    show(newValue) {
      if (newValue) {
        if (this.character) { 
          this.formData = { ...this.character };
        } else { 
          this.resetForm();
        }
        this.modalInstance.show();
      } else {
        this.modalInstance.hide();
      }
    },
  },
  mounted() {
    
    this.modalInstance = new Modal(this.$refs.characterModal, {
      keyboard: false,
      backdrop: 'static',
    });
  },
};
</script>