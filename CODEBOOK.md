# Codebook for Kotlin Inference Study

## Substitutions Available

 - `{@escape@}`
: Logic to escape filenames for output to avoid errors with special characters in CSV-ification process.

 - `{@project-filter@}`
: Filter projects to remove those which are not relevant or should be excluded.

 - `{@time-out@}`
: Output index descriptor for time-based queries.

 - `{@time-part@}`
: Output of current revision and current time for time-based queries.

 - `{@time-or-snapshot@}`
: Either snapshot or at each revision, output base files.

## Output Files

### `dupes.csv`

1. `hash`
: AST Hash of the file at HEAD, `long`.

2. `project`
: Project ID, `string`/`integer`.

3. `url`
: Filename relative to repository root, `string`.

### `basic-usage.csv`

1. `project` (`string`/`integer`)
: Project ID.

2. `file` (`string`)
: Filename relative to repository root.

3. `location` (`string`, *restricted*)
: Overall location of declaration, `string`, one of
   - `return_val`
   - `lambda_arg`
   - `body`
   - `module`

4. `isval` (`boolean`)
: Whether or not location is declared as `val` (`true` if `val`, `false` if `var`).

5. `isinferred` (`boolean`)
: Whether or not the location uses type inference.

6. `count` (`long`)
: Number of declarations fitting items 1--5.

### `over-time.txt`

1. `project` (`string`/`integer`)
: Project ID.

2. `revision` (`string`)
: SHA of revision collected.

3. `time` (`long`)
: Time of revision as microseconds since Unix epoch.

4. `file` (`string`)
: Filename relative to repository root.

5. `location` (`string`, *restricted*)
: Overall location of declaration, *see `basic-usage.csv`/`location`*.

6. `isval` (`boolean`)
: Whether or not location is declared as `val` (`true` if `val`, `false` if `var`).

7. `isinferred` (`boolean`)
: Whether or not the location uses type inference.

8. `count` (`long`)
: Number of declarations fitting items 1--7.

### `gather-rhs-type-information.csv`

1. `project` (`string`/`integer`)
: Project ID.

2. `file` (`string`)
: Filename relative to repository root.

3. `fqn` (`string`)
: Fully qualified name.

4. `isReturnType` (`boolean`)
: Whether or not the type is a declaration type or method return type.

5. `type` (`string`)
: Return either declaration type of method return type.

### `determine-rhs-expression-types.csv`

1. `project` (`string`/`integer`)
: Project ID.

2. `file` (`string`)
: Filename relative to repository root.

3. `class` (`string`)
: Fully qualified name.

4. `isinferred` (`boolean`)
: Whether or not the location uses type inference.

5. `isactualvar` (`boolean`)
: `true` if initializer kind is a `VARRACCES` and not a key in the `vartypes` map (map of declarations from other nodes than the variable node), otherwise returns `false`.

6. `expkind` (`string`)
: `kind` of the initializer in the `Variable` node.

7. `vartype` (`string`)
: Type of `Variable`.

8. `mapval` (`string`)
: `value` (`kind` of node) that corresponds to a `key` (`Variable` name) in the map of declarations, where the declaration is made in nodes other than the `Variable` node.

9. `count` (`long`)
: Number of declarations fitting items 1--7.

### `survival.csv`

### `count-unfiltered.csv`, `count-filtered.csv`

1. `type` (`string`, *restricted*)
: The type of `count`.  Possible values are
    - `projects`
    - `total_files_head`
    - `analyzed_files_head`
    - `total_files_hist`
    - `analyzed_files_hist`

2. `filtered` (`boolean`)
: Whether or not count is from filtered data.

3. `count` (`long`)
: Count of items described by `type`.
