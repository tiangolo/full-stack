import { shallowMount } from '@vue/test-utils';
import UploadButton from '@/components/UploadButton.vue';

describe('UploadButton.vue', () => {
  it('renders props.title when passed', () => {
    const title = 'upload a file';
    const wrapper = shallowMount(UploadButton, {
      propsData: { title },
    });
    expect(wrapper.text()).toMatch(title);
  });
});
