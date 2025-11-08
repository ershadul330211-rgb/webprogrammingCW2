<template>
  <div class="modal fade" ref="quoteModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ formTitle }}</h5>
          <button type="button" class="btn-close" @click="closeModal"></button>
        </div>
        <form @submit.prevent="submitForm">
          <div class="modal-body">
            <div class="mb-3">
              <label for="quoteText" class="form-label">Quote</label>
              <textarea class="form-control" id="quoteText" rows="5" v-model="formData.text" required></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal">
              Close
            </button>
            <button type="submit" class="btn btn-primary">
              Save Quote
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
// Import Modal JS from bootstrap
import { Modal } from 'bootstrap';

export default {
  name: 'QuoteModal',
  props: {
    show: Boolean,
    quote: Object, 
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
      return this.quote ? 'Edit Quote' : 'Add New Quote';
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
        text: '',
      };
    },
  },
  watch: {
    show(newValue) {
      if (newValue) {
        if (this.quote) { // Editing
          this.formData = { ...this.quote };
        } else { // Creating
          this.resetForm();
        }
        this.modalInstance.show();
      } else {
        this.modalInstance.hide();
      }
    },
  },
  mounted() {
    // Initialize the Bootstrap Modal
    this.modalInstance = new Modal(this.$refs.quoteModal, {
      keyboard: false,
      backdrop: 'static',
    });
  },
};
</script>