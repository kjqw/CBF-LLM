# メモ

## データセットをダウンロードする際のエラー

`ControlledLLM/CBFLLM-3.py` で `ds = datasets.load_dataset("Anthropic/hh-rlhf", data_dir="harmless-base")["train"]` を実行すると、以下のエラーが発生した。

```sh
{
 "name": "NonMatchingSplitsSizesError",
 "message": "[{'expected': SplitInfo(name='train', num_bytes=308571371, num_examples=160800, shard_lengths=None, dataset_name='hh-rlhf'), 'recorded': SplitInfo(name='train', num_bytes=56295642, num_examples=42537, shard_lengths=None, dataset_name='hh-rlhf')}, {'expected': SplitInfo(name='test', num_bytes=16562065, num_examples=8552, shard_lengths=None, dataset_name='hh-rlhf'), 'recorded': SplitInfo(name='test', num_bytes=3177260, num_examples=2312, shard_lengths=None, dataset_name='hh-rlhf')}]",
 "stack": "---------------------------------------------------------------------------
NonMatchingSplitsSizesError               Traceback (most recent call last)
File /workspace/cbf-llm/ControlledLLM/CBFLLM-3.py:2
      1 # %%
----> 2 ds = datasets.load_dataset(\"Anthropic/hh-rlhf\", data_dir=\"harmless-base\")[\"train\"]

File /opt/conda/lib/python3.11/site-packages/datasets/load.py:2609, in load_dataset(path, name, data_dir, data_files, split, cache_dir, features, download_config, download_mode, verification_mode, ignore_verifications, keep_in_memory, save_infos, revision, token, use_auth_token, task, streaming, num_proc, storage_options, trust_remote_code, **config_kwargs)
   2606     return builder_instance.as_streaming_dataset(split=split)
   2608 # Download and prepare data
-> 2609 builder_instance.download_and_prepare(
   2610     download_config=download_config,
   2611     download_mode=download_mode,
   2612     verification_mode=verification_mode,
   2613     num_proc=num_proc,
   2614     storage_options=storage_options,
   2615 )
   2617 # Build dataset for splits
   2618 keep_in_memory = (
   2619     keep_in_memory if keep_in_memory is not None else is_small_dataset(builder_instance.info.dataset_size)
   2620 )

File /opt/conda/lib/python3.11/site-packages/datasets/builder.py:1027, in DatasetBuilder.download_and_prepare(self, output_dir, download_config, download_mode, verification_mode, ignore_verifications, try_from_hf_gcs, dl_manager, base_path, use_auth_token, file_format, max_shard_size, num_proc, storage_options, **download_and_prepare_kwargs)
   1025     if num_proc is not None:
   1026         prepare_split_kwargs[\"num_proc\"] = num_proc
-> 1027     self._download_and_prepare(
   1028         dl_manager=dl_manager,
   1029         verification_mode=verification_mode,
   1030         **prepare_split_kwargs,
   1031         **download_and_prepare_kwargs,
   1032     )
   1033 # Sync info
   1034 self.info.dataset_size = sum(split.num_bytes for split in self.info.splits.values())

File /opt/conda/lib/python3.11/site-packages/datasets/builder.py:1140, in DatasetBuilder._download_and_prepare(self, dl_manager, verification_mode, **prepare_split_kwargs)
   1137     dl_manager.manage_extracted_files()
   1139 if verification_mode == VerificationMode.BASIC_CHECKS or verification_mode == VerificationMode.ALL_CHECKS:
-> 1140     verify_splits(self.info.splits, split_dict)
   1142 # Update the info object with the splits.
   1143 self.info.splits = split_dict

File /opt/conda/lib/python3.11/site-packages/datasets/utils/info_utils.py:101, in verify_splits(expected_splits, recorded_splits)
     95 bad_splits = [
     96     {\"expected\": expected_splits[name], \"recorded\": recorded_splits[name]}
     97     for name in expected_splits
     98     if expected_splits[name].num_examples != recorded_splits[name].num_examples
     99 ]
    100 if len(bad_splits) > 0:
--> 101     raise NonMatchingSplitsSizesError(str(bad_splits))
    102 logger.info(\"All the splits matched successfully.\")

NonMatchingSplitsSizesError: [{'expected': SplitInfo(name='train', num_bytes=308571371, num_examples=160800, shard_lengths=None, dataset_name='hh-rlhf'), 'recorded': SplitInfo(name='train', num_bytes=56295642, num_examples=42537, shard_lengths=None, dataset_name='hh-rlhf')}, {'expected': SplitInfo(name='test', num_bytes=16562065, num_examples=8552, shard_lengths=None, dataset_name='hh-rlhf'), 'recorded': SplitInfo(name='test', num_bytes=3177260, num_examples=2312, shard_lengths=None, dataset_name='hh-rlhf')}]"
}
```
