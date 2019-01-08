class CreateUsers < ActiveRecord::Migration[5.2]
  def change
    create_table :users do |t|
      t.integer :chat_id
      t.integer :stage
    end
  end
end
